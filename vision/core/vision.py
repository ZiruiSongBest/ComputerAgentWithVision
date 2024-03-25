from typing import List, Dict, Union, Any
from friday.action.get_os_version import get_os_name
from vision.llm.openai import OpenAIProvider
from vision.core.vision_planner import VisionPlanner
from vision.core.vision_executor import VisionExecutor
from vision.grounding.seeclick import SeeClick
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
1. click
2. click_and_enter
3. scroll (Move and Scroll?)
4. keyboard
5. observation
6. OCR
'''
class Vision:
    def __init__(self, llm_provider_config_path: str = "./vision/config/openai_config.json", logger: Logger = None) -> None:
        # Helpers
        self.llm_provider: OpenAIProvider = OpenAIProvider()
        self.llm_provider.init_provider(llm_provider_config_path)
        self.seeclick = SeeClick()
        self.screen_helper = ScreenHelper()
        self.key_tool = IOEnvironment()
        self.logger = Logger() if logger is None else logger
        
        # submodules
        self.vision_planner = VisionPlanner(llm_provider=self.llm_provider, seeclick=self.seeclick, screen_helper=self.screen_helper, logger=self.logger)
        self.vision_executor = VisionExecutor()
        
        # variables
        self.system_version = get_os_name()
    
    def plan_task(self, task: dict) -> None:
        # Extract task details
        task_name = task.get("name")
        task_description = task.get("description")
        task_type = task.get("type")

        # Log task initiation
        self.logger.log(f"VISION Planning task: {task_name}")
        
        self.vision_planner.plan_task(task)

    def execute_task(self, task: dict) -> dict:
        # Extract task details
        task_name = task.get("name")
        task_description = task.get("description")
        task_type = task.get("type")

        # Log task initiation
        self.logger.log(f"VISION Executing task: {task_name}")

        # Execute task
        return self.vision_executor.execute_task(task)
    
    def execute_tasks(self, tasks: List[dict]) -> List[dict]:
        return [self.execute_task(task) for task in tasks]