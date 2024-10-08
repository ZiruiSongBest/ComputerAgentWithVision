import json
import re
import copy
from friday.core.action_node import ActionNode
from typing import List, Dict, Union, Any
from vision.llm.openai import OpenAIProvider
from vision.grounding.seeclick import SeeClick
from vision.grounding.omnilmm import OmniLMM
from utils.encode_image import encode_data_to_base64_path, encode_single_data_to_base64
from utils.screen_helper import ScreenHelper
from utils.logger import Logger
from utils import json_utils
from vision.prompt.prompt import prompt
from PIL import Image


'''
1. 访问llm
2. 拼接图像, prompt
3. 生成task(定义task类)
'''
class VisionPlanner:
    def __init__(self, template_file_path: str = None, llm_provider: OpenAIProvider = None, seeclick: SeeClick = None, omnilmm: OmniLMM = None, screen_helper: ScreenHelper = None, system_version: str = None, logger: Logger = None) -> None:
        # Helpers
        self.llm_provider = llm_provider
        self.seeclick = seeclick
        self.omnilmm = omnilmm
        self.screen_helper = screen_helper
        self.logger = logger
        
        # templates
        self.templates: Dict[str, str] = {}
        self._init_templates(template_file_path)
        
        # variables
        self.action_num = 0
        self.replan_count = 0
        self.reflection = None
        self.messages: List[Dict[str, Any]] = []
        self.system_version = system_version
        self.vision_tasks = [] # list of task names, execute_list
        self.vision_nodes = {} # dict of task name: ActionNode, action_node

    def _init_templates(self, template_file_path) -> None:
        if template_file_path:
            with open(template_file_path, 'r') as f:
                self.templates = json.load(f)
        else:
            self.templates = prompt
    
    def init_system_messages(self, template_name: str) -> None:
        self.messages = [{
            "role": "system",
            "content": self.templates.get(template_name, "default")
        }]
    
    def plan_task(self, task, pre_task_info, task_names, task_descriptions, next_task):
        '''
            Get a task from Friday, and plan the vision task with vision planner
        
        Args:
            param1 (dict): task from Friday
        
        Returns:
            None
        '''
        'Given the task and the information provided from the previous actions, it\'s clear that the initial approach to find the brand of the webcam used on the laptop embedded in the cupola of the ISS through API calls did not yield the specific information required. The content loaded from the Wikipedia page about the Cupola module on the ISS contains detailed information about the module itself but does not specify the brand of the webcam.\n\nSince the API approach has been exhausted without success, and considering the specificity of the information required, a Vision-based approach might be more suitable. This could involve visually identifying the webcam through images or videos available online that showcase the laptop setup within the Cupola. However, this task requires access to a vast array of visual data and the ability to recognize and identify specific hardware brands from images, which falls outside the capabilities provided here.\n\nGiven the constraints and the nature of the task, it\'s not feasible to accurately determine the brand of the webcam used on the laptop in the Cupola of the ISS with the available methods and information. Therefore, the appropriate response is:\n\n"I can\'t help."'
        if self.replan_count == 0:
            plan_task_message = self.task_decompose_format_message(task, pre_task_info, task_names, task_descriptions, next_task)
        else:
            plan_task_message = self.task_replan_format_message(task)
        
        # TESTCASE TEMP COMMENTED
        response = self.llm_provider.create_completion(plan_task_message)
        self.logger.info(response)
        decomposed_tasks = self.extract_decomposed_tasks(response[0])
        self.logger.info(json.dumps(decomposed_tasks, indent=4), title='Decomposed Tasks', color='green')
        self.logger.write_json(decomposed_tasks, 'vision_planned_formatted.json')
        
        # with open("testcase/vision_plan_formatted3.json", "r") as f:
        #     decomposed_tasks = json.load(f)
        
        self.logger.info(decomposed_tasks, title='Vision Planned Tasks', color='green')
        
        for _, task_info in decomposed_tasks.items():
            self.action_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_deatil = task_info['detail']
            # task_dependencies = task_info['dependencies']
            self.vision_tasks.append(task_name)
            self.vision_nodes[task_name] = ActionNode(task_name, task_description, task_type, task_deatil)
    
    def task_decompose_format_message(self, task, pre_task_info, task_names, task_descriptions, next_task):
        '''
            Send decompose task prompt to LLM and get task list.
            This compose of:
                1. pre_task_info
                2. current image information
                3. current task description with system prompt
        '''
        
        # system_prompt = self.templates.get("plan_task", "default")
        system_prompt = self.templates.get("_SYSTEM_PLAN_PROMPT", "default")
        user_prompt = self.templates.get("_USER_PLAN_PROMPT", "default")
        all_tasks = ""
        for task_name, task_description in zip(task_names, task_descriptions):
            all_tasks += task_name + ": " + task_description + "\n"
        
        # user_prompt = self.templates.get("plan_task_user_prompt", "default")
        user_prompt = user_prompt.format(
            # overall_task = task,
            # pre_task_info = pre_task_info,
            all_task_info = all_tasks,
            next_action = next_task,
            system_version = self.system_version
        )
        
        if self.replan_count > 0:
            system_prompt = self.templates.get("_SYSTEM_REPLAN_PROMPT", "default")
            user_prompt += "\nThe previous task execution failed. Here's the reflection for failed run: \n" + self.reflection + "\n"
        
        current_image = self.screen_helper.capture()
        current_image_base64 = current_image['base64']

        self.message = [
            {
                "role": "system", 
                "content": system_prompt # 作为planner的sys prompt
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": f"Over all task goal: {task}\nprevious task information: {pre_task_info}" # 加入pre_task_info
                    },
                    {
                        "type": "text",
                        "text": "Current Screenshot:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": current_image_base64,    # 给出当前状态的截图
                            # "detail": "low"
                        }
                    },
                    {
                        "type": "text",
                        "text": user_prompt # 给出我想要这一步做什么的task和描述
                    }
                ]
            },
        ]

        json_utils.save_json(self.message, "decompose_task_message.json")
        return self.message
    
    def update_action(self, action, return_val='', relevant_code=None, status=False, type='Code'):
        """
        Update action node info.
        """
        # if type=='Observe':
        #     self.vision_nodes[action]._return_val = return_val
        if return_val != 'None':
            self.vision_nodes[action]._return_val = return_val
        if relevant_code:
            self.vision_nodes[action]._relevant_code = relevant_code
        self.vision_nodes[action]._status = status
        return
    
    def get_pre_tasks_info(self, current_task, observe_only = False): # 传入的是action
        """
        Get string information of the prerequisite task for the current task.
        """
        pre_tasks_info = {}
        for task in self.vision_tasks:
            if task == current_task:
                break
            if observe_only and self.vision_nodes[task].type != 'Observe':
                continue
            task_info = {
                "description" : self.vision_nodes[task].description,
                "return_val" : self.vision_nodes[task].return_val
            }
            pre_tasks_info[task] = task_info
        pre_tasks_info = json.dumps(pre_tasks_info, indent=4)
        return pre_tasks_info
    
    def seeclick_task_planner(self, task_description):
        user_prompt = f"Given the Current Screenshot, Tell me what should I click on to achieve [{task_description}]? Please use a short, comprehend sentence to describe the target. Warp your answer in [answer content]. For example, [Click on the red button]', '[Click on the image with a panda on it]'. "
        response = self.omnilmm.get_response(user_prompt)
        pattern = r"(?:\'(.*?)\'|\"(.*?)\"|\[(.*?)\])"
        matches = re.findall(pattern, response)
        if matches:
            quoted_content = [item for sublist in matches for item in sublist if item]
            return quoted_content[0]
        else:
            # If no quoted content is found, return the whole sentence
            return response
        
    
    def extract_decomposed_tasks(self, response) -> List[Dict[str, Any]]:
        # Improved regular expression to find JSON data within a string
        json_regex = r'```json\s*\n\{[\s\S]*?\n\}\s*```'
        
        # Search for JSON data in the text
        matches = re.findall(json_regex, response)

        # Extract and parse the JSON data if found
        if matches:
            # Removing the ```json and ``` from the match to parse it as JSON
            json_data = matches[0].replace('```json', '').replace('```', '').strip()
            try:
                # Parse the JSON data
                parsed_json = json.loads(json_data)
                return parsed_json
            except json.JSONDecodeError as e:
                return f"Error parsing JSON data: {e}"
        else:
            return "No JSON data found in the string."

    def plan_next_step(self, current_task_info, pre_task_info):
        '''
            Plan the next step of the task
        '''
        system_prompt = self.templates.get("_SYSTEM_NEXT_PROMPT", "default")
        user_prompt = self.templates.get("_USER_NEXT_PROMPT", "default")
        
        user_prompt = user_prompt.format(
            current_task_info = current_task_info,
            pre_task_info = pre_task_info,
            system_version = self.system_version
        )
        
        captured = self.screen_helper.capture()
        current_screen = encode_single_data_to_base64(captured['image'])
        messages = []
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": system_prompt
                }, 
                {
                    "type": "image_url",
                    "image_url": {
                        "url": current_screen
                    }
                },
                {
                    "type": "text",
                    "text": user_prompt
                }
            ]
        })
        
        self.llm_provider.create_completion(messages)

    @staticmethod
    def simple_prompt_construction(system_prompt: str, image: Any, user_prompt: str) -> Dict[str, Any]:
        encoded_image: List[str] = encode_data_to_base64_path(image)
        return {
            "system": system_prompt,
            "image": encoded_image[0],
            "user_prompt": user_prompt
        }

    @staticmethod
    def prompt_construction(system_prompt: str, image_list: List[Any], user_prompt: str, include_last_screenshot: bool = False) -> List[Dict[str, Any]]:
        prompt_message: List[Dict[str, Any]] = [{"role": "system", "content": system_prompt}] if system_prompt else []

        screenshot_text: List[str] = ["Screenshot for the last step:"] if include_last_screenshot else []
        screenshot_text += ["Current Screenshots:", "Annotated Screenshot:"]

        message: List[Dict[str, Any]] = []
        for i, image in enumerate(image_list):
            encoded_image: List[str] = encode_data_to_base64_path(image)
            message.extend([
                {"type": "text", "text": screenshot_text[i]},
                {"type": "image_url", "image_url": {"url": encoded_image[0]}}
            ])
        message.append({"type": "text", "text": user_prompt})
        prompt_message.append({"role": "user", "content": message})

        return prompt_message
