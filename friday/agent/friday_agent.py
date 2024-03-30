from friday.agent.base_agent import BaseAgent
from friday.core.action_node import ActionNode
from collections import defaultdict, deque
from friday.environment.py_env import PythonEnv
from friday.core.llms import OpenAI
from friday.core.action_manager import ActionManager
from friday.action.get_os_version import get_os_version, check_os_version
from friday.agent.prompt import prompt
from friday.core.utils import get_open_api_description_pair, get_open_api_doc_path
from utils import json_utils
import re
import json
from utils.logger import Logger
import copy
from pathlib import Path

class FridayAgent(BaseAgent):
    """ AI agent class, including planning, retrieval and execution modules """

    def __init__(self, config_path=None, action_lib_dir=None, max_iter=3, logger:Logger=None):
        super().__init__()
        self.llm = OpenAI(config_path)
        self.action_lib = ActionManager(config_path, action_lib_dir)
        self.environment = PythonEnv()
        self.prompt = prompt
        self.system_version = get_os_version()
        self.planner = PlanningModule(self.llm, self.environment, self.action_lib, self.prompt['planning_prompt'], self.system_version, logger)
        self.retriever = RetrievalModule(self.llm, self.environment, self.action_lib, self.prompt['retrieve_prompt'], logger)
        self.executor = ExecutionModule(self.llm, self.environment, self.action_lib, self.prompt['execute_prompt'], self.system_version, max_iter, logger)
        self.logging = logger
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)

class PlanningModule(BaseAgent):
    """ The planning module is responsible for breaking down complex tasks into subtasks, re-planning, etc. """

    def __init__(self, llm, environment, action_lib, prompt, system_version, logger:Logger=None):
        """
        Module initialization, including setting the execution environment, initializing prompts, etc.
        """
        super().__init__()
        # Model, environment, database
        self.llm = llm
        self.environment = environment
        self.action_lib = action_lib
        self.system_version = system_version
        self.prompt = prompt
        # Action nodes, action graph information and action topology sorting
        self.action_num = 0
        self.action_node = {}
        self.action_graph = defaultdict(list)
        self.execute_list = []
        self.logging = logger

    def decompose_task(self, task, action_description_pair):
        """
        Implement task disassembly logic.
        """
        
        # TESTCASE TEMP COMMENTED

        files_and_folders = self.environment.list_working_dir()
        action_description_pair = json.dumps(action_description_pair)
        response = self.task_decompose_format_message(task, action_description_pair, files_and_folders)

        # json_utils.save_json(json_utils.json_append(copy.deepcopy(response), 'task', task), f'friday_planned_response.json', indent=4)
        
        self.logging.info(f"The overall response is: {response}", title='Original Response', color='gray')
        decompose_json = self.extract_json_from_string(response)
        
        self.logging.write_json(decompose_json)
        # json_utils.save_json(json_utils.json_append(copy.deepcopy(decompose_json), 'task', task), f'friday_planned_formatted.json', indent=4)
        self.logging.info(f"{decompose_json}", title='Decompose Task', color='gray')

        
        # with open('testcase/planner_response_formatted.json') as f:
        #     decompose_json = json.load(f)
        
        # Building action graph and topological ordering of actions
        self.create_action_graph(decompose_json)
        self.topological_sort()

    def replan_task(self, reasoning, current_task, relevant_action_description_pair):
        """
        replan new task to origin action graph .
        """
        # current_task information
        current_action = self.action_node[current_task] # action_node
        current_task_description = current_action.description # description
        relevant_action_description_pair = json.dumps(relevant_action_description_pair) # no need
        files_and_folders = self.environment.list_working_dir() # current image
        response = self.task_replan_format_message(reasoning, current_task, current_task_description, relevant_action_description_pair, files_and_folders)
        new_action = self.extract_json_from_string(response)
        # add new action to action graph
        self.add_new_action(new_action, current_task)
        # update topological sort
        self.topological_sort()

    def update_action(self, action, return_val='', relevant_code=None, status=False, type='Code'):
        """
        Update action node info.
        """
        if return_val:
            if type=='Code':
                return_val = self.extract_information(return_val, "<return>", "</return>")
                print("************************<return>**************************")
                self.logging.info(return_val, title='Return Value', color='gray')
                print(return_val)
                print("************************</return>*************************")  
            if return_val != 'None':
                self.action_node[action]._return_val = return_val
        if relevant_code:
            self.action_node[action]._relevant_code = relevant_code
        self.action_node[action]._status = status

    def task_decompose_format_message(self, task, action_list, files_and_folders):
        """
        Send decompse task prompt to LLM and get task list.
        """
        api_list = get_open_api_description_pair()
        sys_prompt = self.prompt['_SYSTEM_TASK_DECOMPOSE_PROMPT']
        user_prompt = self.prompt['_USER_TASK_DECOMPOSE_PROMPT'].format(
            system_version=self.system_version,
            task=task,
            action_list = action_list,
            api_list = api_list,
            working_dir = self.environment.working_dir,
            files_and_folders = files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        # json_utils.save_json(json_utils.json_append(copy.deepcopy(self.message), 'task', task), f'friday_planner_plan.json', indent=4)
        
        return self.llm.chat(self.message)
      
    def task_replan_format_message(self, reasoning, current_task, current_task_description, action_list, files_and_folders):
        """
        Send replan task prompt to LLM and get task list.
        """
        sys_prompt = self.prompt['_SYSTEM_TASK_REPLAN_PROMPT']
        user_prompt = self.prompt['_USER_TASK_REPLAN_PROMPT'].format(
            current_task = current_task,
            current_task_description = current_task_description,
            system_version=self.system_version,
            reasoning = reasoning,
            action_list = action_list,
            working_dir = self.environment.working_dir,
            files_and_folders = files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    def get_action_list(self, relevant_action=None):
        """
        Get action list, including action names and descriptions.
        """
        action_dict = self.action_lib.descriptions
        if not relevant_action:
            return json.dumps(action_dict)
        relevant_action_dict = {action : description for action ,description in action_dict.items() if action in relevant_action}
        relevant_action_list = json.dumps(relevant_action_dict)
        return relevant_action_list
    
    def create_action_graph(self, decompose_json):
        """
        Creates a action graph from a list of dependencies.
        """
        # generate execte graph
        for _, task_info in decompose_json.items():
            self.action_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_dependencies = task_info['dependencies']
            self.action_node[task_name] = ActionNode(task_name, task_description, task_type)
            self.action_graph[task_name] = task_dependencies
            for pre_action in self.action_graph[task_name]:
                self.action_node[pre_action].next_action[task_name] = task_description

    
    def add_new_action(self, new_task_json, current_task):
        """
        Creates a action graph from a list of dependencies.
        """
        # update execte graph
        for _, task_info in new_task_json.items():
            self.action_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_dependencies = task_info['dependencies']
            self.action_node[task_name] = ActionNode(task_name, task_description, task_type)
            self.action_graph[task_name] = task_dependencies
            for pre_action in self.action_graph[task_name]:
                self.action_node[pre_action].next_action[task_name] = task_description           
        last_new_task = list(new_task_json.keys())[-1]
        self.action_graph[current_task].append(last_new_task)

    def topological_sort(self):
        """
        generate graph topological sort.
        """
        # init execute list
        self.execute_list = []
        graph = defaultdict(list)
        for node, dependencies in self.action_graph.items():
            # If the current node has not been executed, put it in the dependency graph.
            if not self.action_node[node].status:
                graph.setdefault(node, [])
                for dependent in dependencies:
                    # If the dependencies of the current node have not been executed, put them in the dependency graph.
                    if not self.action_node[dependent].status:
                        graph[dependent].append(node)

        in_degree = {node: 0 for node in graph}      
        # Count in-degree for each node
        for node in graph:
            for dependent in graph[node]:
                in_degree[dependent] += 1

        # Initialize queue with nodes having in-degree 0
        queue = deque([node for node in in_degree if in_degree[node] == 0])

        # List to store the order of execution

        while queue:
            # Get one node with in-degree 0
            current = queue.popleft()
            self.execute_list.append(current)

            # Decrease in-degree for all nodes dependent on current
            for dependent in graph[current]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Check if topological sort is possible (i.e., no cycle)
        if len(self.execute_list) == len(graph):
            print("topological sort is possible")
        else:
            return "Cycle detected in the graph, topological sort not possible."
        
    def get_pre_tasks_info(self, current_task):
        """
        Get string information of the prerequisite task for the current task.
        """
        pre_tasks_info = {}
        for task in self.action_graph[current_task]:
            task_info = {
                "description" : self.action_node[task].description,
                "return_val" : self.action_node[task].return_val
            }
            pre_tasks_info[task] = task_info
        pre_tasks_info = json.dumps(pre_tasks_info)
        return pre_tasks_info



class RetrievalModule(BaseAgent):
    """ Retrieval module, responsible for retrieving available actions in the action library. """

    def __init__(self, llm, environment, action_lib, prompt, logger:Logger=None):
        """
        Module initialization, including setting the execution environment, initializing prompts, etc.
        """
        super().__init__()
        # Model, environment, database
        self.llm = llm
        self.environment = environment
        self.action_lib = action_lib
        self.prompt = prompt
        self.logging = logger

    def delete_action(self, action):
        """
        Delete relevant action content, including code, description, parameter information, etc.
        """
        self.action_lib.delete_action(action)

    def retrieve_action_name(self, task, k=10):        
        """
        Implement retrieval action name logic
        """
        retrieve_action_name = self.action_lib.retrieve_action_name(task, k)
        return retrieve_action_name

    def action_code_filter(self, action_code_pair, task):
        """
        Implement filtering of search codes.
        """
        action_code_pair = json.dumps(action_code_pair)
        response = self.action_code_filter_format_message(action_code_pair, task)
        action_name = self.extract_information(response, '<action>', '</action>')[0]
        code = ''
        if action_name:
            code = self.action_lib.get_action_code(action_name)
        return code

    def retrieve_action_description(self, action_name):
        """
        Implement search action description logic.
        """
        retrieve_action_description = self.action_lib.retrieve_action_description(action_name)
        return retrieve_action_description  

    def retrieve_action_code(self, action_name):
        """
        Implement retrieval action code logic.
        """
        retrieve_action_code = self.action_lib.retrieve_action_code(action_name)
        return retrieve_action_code 
    
    def retrieve_action_code_pair(self, retrieve_action_name):
        """
        Retrieve task code pairs.
        """
        retrieve_action_code = self.retrieve_action_code(retrieve_action_name)
        action_code_pair = {}
        for name, description in zip(retrieve_action_name, retrieve_action_code):
            action_code_pair[name] = description
        return action_code_pair        
        
    def retrieve_action_description_pair(self, retrieve_action_name):
        """
        Retrieve task description pairs.
        """
        retrieve_action_description = self.retrieve_action_description(retrieve_action_name)
        action_description_pair = {}
        for name, description in zip(retrieve_action_name, retrieve_action_description):
            action_description_pair[name] = description
        return action_description_pair
    
    def action_code_filter_format_message(self, action_code_pair, task_description):
        """
        Send aciton code to llm to filter useless action codes.
        """
        sys_prompt = self.prompt['_SYSTEM_ACTION_CODE_FILTER_PROMPT']
        user_prompt = self.prompt['_USER_ACTION_CODE_FILTER_PROMPT'].format(
            task_description=task_description,
            action_code_pair=action_code_pair
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)    


class ExecutionModule(BaseAgent):
    """ Execution module, responsible for executing actions and updating the action library """

    def __init__(self, llm, environment, action_lib, prompt, system_version, max_iter, logger:Logger=None):
        '''
        Module initialization, including setting the execution environment, initializing prompts, etc.
        '''
        super().__init__()
        self.llm = llm
        self.environment = environment
        self.action_lib = action_lib
        self.system_version = system_version
        self.prompt = prompt
        self.max_iter = max_iter
        self.open_api_doc_path = get_open_api_doc_path()
        self.open_api_doc = {}
        self.logging = logger
        with open(self.open_api_doc_path) as f:
            self.open_api_doc = json.load(f) 
    
    def generate_action(self, task_name, task_description, pre_tasks_info, relevant_code):
        '''
        Generate action code logic, generate code that can complete the action and its calls.
        '''
        relevant_code = json.dumps(relevant_code)
        create_msg = self.skill_create_and_invoke_format_message(task_name, task_description, pre_tasks_info, relevant_code)
        code = self.extract_python_code(create_msg)
        invoke = self.extract_information(create_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        return code, invoke

    # def generate_action(self, task_name, task_description):
    #     '''
    #     Generate action code logic, generate code that can complete the action and its calls.
    #     '''
    #     create_msg = self.skill_create_format_message(task_name, task_description)
    #     code = self.extract_python_code(create_msg)
    #     return code

    def execute_action(self, code, invoke, type):
        '''
        Implement action execution logic.
        instantiate the action class and execute it, and return the execution completed status.
        '''
        # print result info
        if type == 'Code':
            info = "\n" + '''print("<return>")''' + "\n" + "print(result)" +  "\n" + '''print("</return>")'''
            code = code + '\nresult=' + invoke + info
        self.logging.info("************************<code>**************************")
        self.logging.info(code, title='Code', color='gray')
        self.logging.info("************************</code>*************************")
        state = self.environment.step(code)
        self.logging.info("************************<state>**************************")
        output = {
            "result": state.result,
            "error": state.error
        }
        self.logging.info(json.dumps(output, indent=4), title='Execution Result', color='gray')
        # self.logging.info("error: " + state.error + "\nresult: " + state.result + "\npwd: " + state.pwd + "\nls: " + state.ls)
        self.logging.info("************************</state>*************************")
        return state

    def judge_action(self, code, task_description, state, next_action):
        '''
        Implement action judgment logic.
        judge whether the action completes the current task, and return the JSON result of the judgment.
        '''
        judge_json = self.task_judge_format_message(code, task_description, state.result, state.pwd, state.ls, next_action)
        reasoning = judge_json['reasoning']
        judge = judge_json['judge']
        score = judge_json['score']
        return reasoning, judge, score

    def amend_action(self, current_code, task_description, state, critique, pre_tasks_info):
        '''
        Implement action repair logic.
        repair unfinished tasks or erroneous code, and return the repaired code and call.
        '''
        amend_msg = self.skill_amend_and_invoke_format_message(current_code, task_description, state.error, state.result, state.pwd, state.ls, critique, pre_tasks_info)
        new_code = self.extract_python_code(amend_msg)
        invoke = self.extract_information(amend_msg, begin_str='<invoke>', end_str='</invoke>')[0]
        return new_code, invoke

    def analysis_action(self, code, task_description, state):
        '''
        Implement the analysis of code errors. 
        If it is an environmental error that requires new operations, go to the planning module. 
        Otherwise, hand it to amend_action and return JSON.
        '''
        analysis_json = self.error_analysis_format_message(code, task_description, state.error, state.pwd, state.ls)
        reasoning = analysis_json['reasoning']
        type = analysis_json['type']
        return reasoning, type
        
    def store_action(self, action, code):
        """
        Store action code and info.
        
        """
        # If action not in db.
        if not self.action_lib.exist_action(action):
            # Implement action storage logic and store new actions
            args_description = self.extract_args_description(code)
            action_description = self.extract_action_description(code)
            # Save action name, code, and description to JSON
            action_info = self.save_action_info_to_json(action, code, action_description)
            # Save code and descriptions to databases and JSON files
            self.action_lib.add_new_action(action_info)
            # Parameter description save path
            args_description_file_path = self.action_lib.action_lib_dir + '/args_description/' + action + '.txt'      
            # save args_description
            self.save_str_to_path(args_description, args_description_file_path)
        else:
            print("action already exists!")


    def api_action(self, description, api_path, context="No context provided."):
        """
        Call api tool to execute task.
        """
        response = self.generate_call_api_format_message(description, api_path, context)
        code = self.extract_python_code(response)
        return code 
    
    def question_and_answer_action(self, context, question, current_question=None):
        """
        Answer questions based on the information found.
        """
        response = self.question_and_answer_format_message(context, question, current_question)
        return response

    def skill_create_and_invoke_format_message(self, task_name, task_description, pre_tasks_info, relevant_code):
        """
        Send skill generate and invoke message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_CREATE_AND_INVOKE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_CREATE_AND_INVOKE_PROMPT'].format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir= self.environment.working_dir,
            task_name=task_name,
            pre_tasks_info=pre_tasks_info,
            relevant_code=relevant_code
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    def skill_create_format_message(self, task_name, task_description):
        """
        Send skill create message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_CREATE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_CREATE_PROMPT'].format(
            system_version=self.system_version,
            task_description=task_description,
            working_dir= self.environment.working_dir,
            task_name=task_name
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)

    def invoke_generate_format_message(self, class_code, task_description, pre_tasks_info):
        """
        Send invoke generate message to LLM.
        """
        class_name, args_description = self.extract_class_name_and_args_description(class_code)
        sys_prompt = self.prompt['_SYSTEM_INVOKE_GENERATE_PROMPT']
        user_prompt = self.prompt['_USER_INVOKE_GENERATE_PROMPT'].format(
            class_name = class_name,
            task_description = task_description,
            args_description = args_description,
            pre_tasks_info = pre_tasks_info,
            working_dir = self.environment.working_dir
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)        
    
    def question_and_answer_format_message(self, context, question, current_question):
        """
        Send QA message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_QA_PROMPT']
        user_prompt = self.prompt['_USER_QA_PROMPT'].format(
            context = context,
            question = question,
            current_question = current_question
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)      
 
    def skill_amend_and_invoke_format_message(self, original_code, task, error, code_output, current_working_dir, files_and_folders, critique, pre_tasks_info):
        """
        Send skill amend message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_AMEND_AND_INVOKE_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_AMEND_AND_INVOKE_PROMPT'].format(
            original_code = original_code,
            task = task,
            error = error,
            code_output = code_output,
            current_working_dir = current_working_dir,
            working_dir= self.environment.working_dir,
            files_and_folders = files_and_folders,
            critique = critique,
            pre_tasks_info = pre_tasks_info
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)   

    def skill_amend_format_message(self, original_code, task, error, code_output, current_working_dir, files_and_folders, critique):
        """
        Send skill amend message to LLM.
        """
        sys_prompt = self.prompt['_SYSTEM_SKILL_AMEND_PROMPT']
        user_prompt = self.prompt['_USER_SKILL_AMEND_PROMPT'].format(
            original_code = original_code,
            task = task,
            error = error,
            code_output = code_output,
            current_working_dir = current_working_dir,
            working_dir= self.environment.working_dir,
            files_and_folders = files_and_folders,
            critique = critique
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.chat(self.message)    
    
    def task_judge_format_message(self, current_code, task, code_output, current_working_dir, files_and_folders, next_action):
        """
        Send task judge prompt to LLM and get JSON response.
        """
        next_action = json.dumps(next_action)
        sys_prompt = self.prompt['_SYSTEM_TASK_JUDGE_PROMPT']
        user_prompt = self.prompt['_USER_TASK_JUDGE_PROMPT'].format(
            current_code=current_code,
            task=task,
            code_output=code_output,
            current_working_dir=current_working_dir,
            working_dir=self.environment.working_dir,
            files_and_folders=files_and_folders,
            next_action=next_action
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response =self.llm.chat(self.message)
        judge_json = self.extract_json_from_string(response)  
        print("************************<judge_json>**************************")
        print(judge_json)
        print("************************</judge_json>*************************")           
        return judge_json    

    def error_analysis_format_message(self, current_code, task, code_error, current_working_dir, files_and_folders):
        """
        Send error analysis prompt to LLM and get JSON response.
        """
        sys_prompt = self.prompt['_SYSTEM_ERROR_ANALYSIS_PROMPT']
        user_prompt = self.prompt['_USER_ERROR_ANALYSIS_PROMPT'].format(
            current_code=current_code,
            task=task,
            code_error=code_error,
            current_working_dir=current_working_dir,
            working_dir= self.environment.working_dir,
            files_and_folders= files_and_folders
        )
        self.message = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response =self.llm.chat(self.message)
        analysis_json = self.extract_json_from_string(response)      
        print("************************<analysis_json>**************************")
        print(analysis_json)
        print("************************</analysis_json>*************************")           
        return analysis_json  

    def extract_python_code(self, response):
        """
        Extract python code from response.
        """
        python_code = ""
        if '```python' in response:
            python_code = response.split('```python')[1].split('```')[0]
        elif '```' in python_code:
            python_code = response.split('```')[1].split('```')[0]
        return python_code    

    def extract_class_name_and_args_description(self, class_code):
        """
        Extract class_name and args description from python code.
        """
        class_name_pattern = r"class (\w+)"
        class_name_match = re.search(class_name_pattern, class_code)
        class_name = class_name_match.group(1) if class_name_match else None

        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None

        return class_name, args_description
    
    def extract_args_description(self, class_code):
        """
        Extract args description from python code.
        """
        # Extracting the __call__ method's docstring
        call_method_docstring_pattern = r"def __call__\([^)]*\):\s+\"\"\"(.*?)\"\"\""
        call_method_docstring_match = re.search(call_method_docstring_pattern, class_code, re.DOTALL)
        args_description = call_method_docstring_match.group(1).strip() if call_method_docstring_match else None
        return args_description

    def extract_action_description(self, class_code):
        """
        Extract action description from python code.
        """
        # Extracting the __init__ method's description
        init_pattern = r"def __init__\s*\(self[^)]*\):\s*(?:.|\n)*?self\._description\s*=\s*\"([^\"]+)\""
        action_match = re.search(init_pattern, class_code, re.DOTALL)
        action_description = action_match.group(1).strip() if action_match else None
        return action_description
    
    def save_str_to_path(self, content, path):
        """
        save str content to the specified path. 
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            lines = content.strip().splitlines()
            content = '\n'.join(lines)
            f.write(content)
                 
    def save_action_info_to_json(self, action, code, description):
        """
        save action info to json. 
        """
        info = {
            "task_name" : action,
            "code": code,
            "description": description
        }
        return info
    
    def generate_call_api_format_message(self, tool_sub_task, tool_api_path, context="No context provided."):
        self.logging.warn(self.generate_openapi_doc_2(tool_api_path), title='OpenAPI Doc')
        self.sys_prompt = self.prompt['_SYSTEM_TOOL_USAGE_PROMPT'].format(
            openapi_doc = json.dumps(self.generate_openapi_doc_2(tool_api_path)),
            tool_sub_task = tool_sub_task,
            context = context
        )
        self.logging.info("************************<openapi_doc>**************************")
        self.logging.info(self.sys_prompt, title='OpenAPI Doc', color='gray')
        
        self.user_prompt = self.prompt['_USER_TOOL_USAGE_PROMPT']
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        self.logging.info(self.message, title='API Call', color='gray')
        return self.llm.chat(self.message)
    
    def generate_openapi_doc_2(self, tool_api_path):
        return self.extract_api_details(self.open_api_doc, tool_api_path)
        
    def generate_openapi_doc(self, tool_api_path):
        """
        Format openapi document.
        """
        # init current api's doc
        curr_api_doc = {}
        json_utils.save_json(self.open_api_doc, 'openapi_doc.json', indent=4)
        curr_api_doc["openapi"] = self.open_api_doc["openapi"]
        curr_api_doc["info"] = self.open_api_doc["info"]
        curr_api_doc["paths"] = {}
        curr_api_doc["components"] = {"schemas":{}}
        api_path_doc = {}
        #extract path and schema
        if tool_api_path not in self.open_api_doc["paths"]:
            curr_api_doc = {"error": "The api is not existed"}
            return curr_api_doc
        api_path_doc = self.open_api_doc["paths"][tool_api_path]
        curr_api_doc["paths"][tool_api_path] = api_path_doc
        find_ptr = {}
        if "get" in api_path_doc:
            findptr  = api_path_doc["get"]
        elif "post" in api_path_doc:
            findptr = api_path_doc["post"]
        api_params_schema_ref = ""
        # json格式
        if (("requestBody" in findptr) and 
        ("content" in findptr["requestBody"]) and 
        ("application/json" in findptr["requestBody"]["content"]) and 
        ("schema" in findptr["requestBody"]["content"]["application/json"]) and 
        ("$ref" in findptr["requestBody"]["content"]["application/json"]["schema"])):
            api_params_schema_ref = findptr["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        elif (("requestBody" in findptr) and 
        ("content" in findptr["requestBody"]) and 
        ("multipart/form-data" in findptr["requestBody"]["content"]) and 
        ("schema" in findptr["requestBody"]["content"]["multipart/form-data"]) and 
        ("allOf" in findptr["requestBody"]["content"]["multipart/form-data"]["schema"]) and 
        ("$ref" in findptr["requestBody"]["content"]["multipart/form-data"]["schema"]["allOf"][0])):
            api_params_schema_ref = findptr["requestBody"]["content"]["multipart/form-data"]["schema"]["allOf"][0]["$ref"]
        if api_params_schema_ref != None and api_params_schema_ref != "":
            curr_api_doc["components"]["schemas"][api_params_schema_ref.split('/')[-1]] = self.open_api_doc["components"]["schemas"][api_params_schema_ref.split('/')[-1]]
        
        # new_api_doc = {}
        # new_api_doc["path"] = tool_api_path
        # method = self.open_api_doc["paths"][tool_api_path][0]
        # if "get" in self.open_api_doc["paths"][tool_api_path]:
        #     method  = "get"
        # elif "post" in self.open_api_doc["paths"][tool_api_path]:
        #     method  = "post"
        # new_api_doc['method'] = method
        # new_api_doc["api_summary"] = curr_api_doc['paths'][tool_api_path][method]['summary']
        # for key, value in curr_api_doc['paths'][tool_api_path][method]["requestBody"]["content"]: # content type
        #     new_api_doc["contentType"] = key
        # new_api_doc["contentType"] = curr_api_doc['paths'][tool_api_path][method]["requestBody"]["content"]
        # details = curr_api_doc['paths'][tool_api_path][method]
        # new_api_doc["Request Body Format"] = list(details['requestBody']['content'].keys())[0]
        return curr_api_doc

    def extract_API_Path(self, text):
        """
        Extracts UNIX-style and Windows-style paths from the given string,
        handling paths that may be enclosed in quotes.

        :param s: The string from which to extract paths.
        :return: A list of extracted paths.
        """
        # Regular expression for UNIX-style and Windows-style paths
        unix_path_pattern = r"/[^/\s]+(?:/[^/\s]*)*"
        windows_path_pattern = r"[a-zA-Z]:\\(?:[^\\\/\s]+\\)*[^\\\/\s]+"

        # Combine both patterns
        pattern = f"({unix_path_pattern})|({windows_path_pattern})"

        # Find all matches
        matches = re.findall(pattern, text)

        # Extract paths from the tuples returned by findall
        paths = [match[0] or match[1] for match in matches]

        # Remove enclosing quotes (single or double) from the paths
        stripped_paths = [path.strip("'\"") for path in paths]
        return stripped_paths[0]
    
    def resolve_ref(self, json_data, ref):
        """Resolves a $ref to its actual definition in the given JSON data."""
        parts = ref.split('/')
        result = json_data
        for part in parts[1:]:  # Skip the first element as it's always '#'
            result = result[part]
        return result

    def extract_types_from_schema_element(self, schema_element):
        """从schema元素中提取类型信息，处理anyOf和直接定义的类型。"""
        if 'type' in schema_element:
            return [schema_element['type']]
        elif 'anyOf' in schema_element:
            types = []
            for sub_element in schema_element['anyOf']:
                types.extend(self.extract_types_from_schema_element(sub_element))
            return types
        else:
            return ['unknown']

    def extract_properties_from_schema(self, schema, json_data):
        """递归地从schema中提取属性和类型信息，处理allOf、anyOf和$ref。"""
        properties = {}
        required = schema.get('required', [])

        if 'allOf' in schema:
            for item in schema['allOf']:
                sub_properties, sub_required = self.extract_properties_from_schema(item, json_data)
                properties.update(sub_properties)
                required.extend(sub_required)
        elif '$ref' in schema:
            ref_schema = self.resolve_ref(json_data, schema['$ref'])
            properties, required = self.extract_properties_from_schema(ref_schema, json_data)
        else:
            properties = schema.get('properties', {})

        return properties, required

    def extract_api_details(self, json_data, api_path):
        api_details = json_data['paths'][api_path]
        for method, details in api_details.items():
            summary = details['summary']
            parameters_information = []
            request_body_format = None
            
            # 提取直接定义的参数
            if 'parameters' in details:
                for param in details['parameters']:
                    parameter_info = {
                        'name': param['name'],
                        'in': param['in'],
                        'required': param.get('required', False),
                        'type': param['schema']['type'] if 'schema' in param else 'unknown'
                    }
                    parameters_information.append(parameter_info)
            
            # 处理requestBody（如果存在）
            if 'requestBody' in details:
                request_body_format = list(details['requestBody']['content'].keys())[0]
                schema_info = details['requestBody']['content'][request_body_format]['schema']
                
                properties, required = self.extract_properties_from_schema(schema_info, json_data)
                
                for prop, prop_details in properties.items():
                    types = self.extract_types_from_schema_element(prop_details)  # 提取参数可能的类型
                    parameter_info = {
                        'name': prop,
                        'type': types,  # 参数可能有多种类型
                        'required': prop in required
                    }
                    parameters_information.append(parameter_info)

            api_details_dict = {
                'api_path': api_path,
                'method': method,
                'summary': summary,
                'parameters': parameters_information,
                'request_body_format': request_body_format
            }
            
            return api_details_dict




if __name__ == '__main__':
    agent = FridayAgent(config_path='../../examples/config.json', action_lib_dir="friday/action_lib")
    print(agent.executor.extract_API_Path('''Use the "/tools/arxiv' API to search for the autogen paper and retrieve its summary.'''))
