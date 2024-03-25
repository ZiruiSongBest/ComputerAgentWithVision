import json
from friday.agent.friday_agent import PlanningModule, ExecutionModule, RetrievalModule
from utils.logger import Logger

class FridayExecutor:
    def __init__(self, planning_agent:PlanningModule, execute_agent:ExecutionModule, retrieve_agent:RetrievalModule, logger:Logger, score):
        self.planning_agent = planning_agent
        self.execute_agent = execute_agent
        self.retrieve_agent = retrieve_agent
        self.logging = logger
        self.score = score

    def handle_qa_type(self, pre_tasks_info, task, description):
        if self.planning_agent.action_num == 1:
            result = self.execute_agent.question_and_answer_action(pre_tasks_info, task, task)
        else:
            result = self.execute_agent.question_and_answer_action(pre_tasks_info, task, description)
        self.logging.info(result, title='QA Result', color='green')

    def retrieve_existing_action(self, description):
        retrieve_name = self.retrieve_agent.retrieve_action_name(description, 3)
        relevant_code = self.retrieve_agent.retrieve_action_code_pair(retrieve_name)
        return relevant_code

    def handle_execution(self, code, invoke, type):
        state = self.execute_agent.execute_action(code, invoke, type)
        
        output = {
            "result": state.result,
            "error": state.error
        }
        if state.error is not None:
            self.logging.error(state.error)
        # else:
        #     self.logging.info(state, title='Execution Result', color='green')
        self.logging.info(f"The subtask result is: {json.dumps(output, indent=4)}", title='Execution Result', color='grey')
        return state
    
    def plan_task(self, task):
        self.logging.info(task, title='Task', color='green')
        # relevant action
        retrieve_action_name = self.retrieve_agent.retrieve_action_name(task)
        retrieve_action_description_pair = self.retrieve_agent.retrieve_action_description_pair(retrieve_action_name)

        # task planner
        self.planning_agent.decompose_task(task, retrieve_action_description_pair)
    

    def execute_task(self, task):
        self.logging.debug("The current task is: {task}".format(task=task))
        action = self.planning_agent.execute_list[0]
        action_node = self.planning_agent.action_node[action]
        description = action_node.description
        self.logging.info("The current subtask is: {subtask}".format(subtask=description), title='Current Subtask', color='green')
        code = ''
        # The return value of the current task
        result = ''
        next_action = action_node.next_action
        type = action_node.type
        pre_tasks_info = self.planning_agent.get_pre_tasks_info(action)
        relevant_code = {}
        
        if type == 'QA':
            self.handle_qa_type(pre_tasks_info, task, description)
        else:
            invoke = ''
            if type == 'API':
                api_path = self.execute_agent.extract_API_Path(description)
                code = self.execute_agent.api_action(description, api_path, pre_tasks_info)
            elif type == 'Code':
                relevant_code = self.retrieve_existing_action(description)
                code, invoke = self.execute_agent.generate_action(action, description, pre_tasks_info, relevant_code)
            state = self.handle_execution(code, invoke, type)
            result = state.result
            
            if type == 'Code':
                need_amend = False
                critique = ''
                if state.error == None:
                    critique, judge, score = self.execute_agent.judge_action(code, description, state, next_action)
                    if not judge:
                        print("critique: {}".format(critique))
                        need_amend = True
                else:
                    #  Determine whether it is caused by an error outside the code
                    reasoning, error_type = self.execute_agent.analysis_action(code, description, state)
                    if error_type == 'replan':
                        relevant_action_name = self.retrieve_agent.retrieve_action_name(reasoning)
                        relevant_action_description_pair = self.retrieve_agent.retrieve_action_description_pair(relevant_action_name)
                        self.planning_agent.replan_task(reasoning, action, relevant_action_description_pair)
                        return ['replan']
                    need_amend = True
                    
                trial_times = 0
                while trial_times < self.execute_agent.max_iter and need_amend:
                    trial_times += 1
                    print(f"current amend times: {trial_times}")
                    new_code, invoke = self.execute_agent.amend_action(code, description, state, critique, pre_tasks_info)
                    code = new_code
                    state = self.handle_execution(code, invoke, type)
                    result = state.result

                    if state.error is None:
                        critique, judge, score = self.execute_agent.judge_action(code, description, state, next_action)
                        if judge:
                            need_amend = False
                    else:
                        need_amend = True  
                
                # If the task still cannot be completed, an error message will be reported.
                if need_amend == True:
                    print("I can't Do this Task!!")
                    return ['fail']
                else: # The task is completed, if code is save the code, args_description, action_description in lib
                    if score >= self.score:
                        self.execute_agent.store_action(action, code)
        return ['success', result, relevant_code]
# Usage example
# friday_executor = FridayExecutor(planning_agent, execute_agent, retrieve_agent)
# friday_executor.execute_task(type, pre_tasks_info, task, description, action, next_action)
