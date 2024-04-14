import time
from typing import List, Dict, Union, Any
from friday.action.get_os_version import get_os_name
from vision.llm.openai import OpenAIProvider
from vision.core.vision_planner import VisionPlanner
from vision.core.vision_executor import VisionExecutor
from vision.grounding.seeclick import SeeClick
from vision.grounding.omnilmm import OmniLMM
from utils.screen_helper import ScreenHelper
from utils.KEY_TOOL import IOEnvironment
from utils.logger import Logger


'''
综合planner和executor
1. 接受来自Friday的task，通过vision planner规划，生成vision task
2. 通过vision executor执行vision task
3. 返回结果
'''

'''
Vision Task Categories:
Click, Enter, Scroll, Observe
# 4. keyboard
# 5. observation
'''
class Vision:
    def __init__(self, llm_provider_config_path: str = "./vision/config/openai_config.json", logger: Logger = None) -> None:
        # Helpers
        self.logger = Logger() if logger is None else logger
        self.llm_provider: OpenAIProvider = OpenAIProvider()
        self.llm_provider.init_provider(llm_provider_config_path)
        self.screen_helper = ScreenHelper()
        self.key_tool = IOEnvironment()
        self.seeclick = SeeClick(screen_helper=self.screen_helper)
        self.omnilmm = OmniLMM(screen_helper=self.screen_helper)
        
        # variables
        self.system_version = get_os_name()
        
        # submodules
        self.vision_planner = VisionPlanner(llm_provider=self.llm_provider, seeclick=self.seeclick, omnilmm=self.omnilmm, screen_helper=self.screen_helper, logger=self.logger)
        self.vision_executor = VisionExecutor(llm_provider=self.llm_provider, seeclick=self.seeclick, omnilmm=self.omnilmm, screen_helper=self.screen_helper, key_tool=self.key_tool, system_version=self.system_version, logger=self.logger)
        
    
    def global_execute(self, task, actions, action_nodes, pre_tasks_info):
        next_action = action_nodes[-1].next_action
        
        descriptions = [action.description for action in action_nodes]

        self.logger.log(f"VISION Global task: {actions[0]}")
        self.vision_planner.plan_task(task, pre_tasks_info, actions, descriptions, next_action)
        
        result, relevant_code = self.execute_list(task, actions)
        
        # status = self.assess_current_task(task, actions, descriptions, result)
        
        # while status == "replan" and self.vision_planner.replan_count < 3:
        #     self.vision_planner.replan_count += 1
        #     self.vision_planner.plan_task(task, actions, descriptions, next_action)
        #     result, relevant_code = self.execute_list(task, actions)
        #     status = self.assess_current_task(task, actions, descriptions, result)
        
        # self.logger.info(status + result, title='Current Vision Task Result', color='green')

        return ['success', result, relevant_code]

    def execute_list(self, task, actions):
        result = ''
        relevant_code = {}

        # Execute task
        for task_name in self.vision_planner.vision_tasks:
            vision_type = self.vision_planner.vision_nodes[task_name].type
            pre_tasks_info = self.vision_planner.get_pre_tasks_info(task_name)
            # self.logger.info(pre_tasks_info, title='Pre-tasks Information', color='grey')
            current_result = self.execute_single_task(task_name)
            self.vision_planner.update_action(task_name, current_result, True, vision_type)
            
            if vision_type == 'Click' or vision_type == 'Enter':
                time.sleep(5)

        result = self.vision_planner.get_pre_tasks_info('end', True)
        
        return result, relevant_code
        
    def execute_single_task(self, task_name) -> dict:
        # Extract task details
        vision_node = self.vision_planner.vision_nodes.get(task_name)
        type = vision_node.type
        next_action = vision_node.next_action
        description = vision_node.description
        content = vision_node.detail
        
        self.logger.info(f"Current VISION Executing task: {task_name}")
        current_result = ''
        if (type == 'Enter'):
            current_result = self.vision_executor.enter(content)
        elif (type == 'Click'):
            current_content = self.vision_planner.seeclick_task_planner(content)
            self.logger.info(f"Clicking on: {current_content}", title='OmniResponse', color='blue')
            current_result = self.vision_executor.click(current_content)
        elif (type == 'Observe'):
            current_result = self.vision_executor.observe(content)
        
        return current_result
    
    def assess_current_task(self, task, task_names, task_descriptions, result):
        '''
            Access the current task from the vision task list.
        '''
        all_tasks = ""
        for task_name, task_description in zip(task_names, task_descriptions):
            all_tasks = task_name + ": " + task_description + "\n"

        user_message = self.vision_planner.templates.get("_USER_TASK_ASSESS_PROMPT", "default")
        user_message = user_message.format(
            over_all_task = task,
            task_and_descriptions = all_tasks,
            result = result
        )
        # response = self.vision_executor.observe(user_message)
        response = self.omnilmm.get_response(user_message)
        
        self.logger.info(response, title='Assess Current Task', color='green')
        
        if "Yes" in response:
            return "success"
        elif "No" in response:
            return "fail"
        
        self.vision_planner.reflection = response
        return "replan"