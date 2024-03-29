import json
import re
from friday.core.action_node import ActionNode
from typing import List, Dict, Union, Any
from vision.llm.openai import OpenAIProvider
from vision.grounding.seeclick import SeeClick
from utils.encode_image import encode_data_to_base64_path, encode_single_data_to_base64
from utils.screen_helper import ScreenHelper
from utils.logger import Logger
from utils.json_utils import save_json
from vision.prompt.prompt import prompt
from PIL import Image


'''
1. 访问llm
2. 拼接图像, prompt
3. 生成task(定义task类)
'''
class VisionPlanner:
    def __init__(self, template_file_path: str = None, llm_provider: OpenAIProvider = None, seeclick: SeeClick = None, screen_helper: ScreenHelper = None, system_version: str = None, logger: Logger = None) -> None:
        # Helpers
        self.llm_provider = llm_provider
        self.seeclick = seeclick
        self.screen_helper = screen_helper
        self.logger = logger
        
        # templates
        self.templates: Dict[str, str] = {}
        self._init_templates(template_file_path)
        
        # variables
        self.action_num = 0
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
    
    def plan_task(self, pre_task_info, task_name, task_description):
        '''
            Get a task from Friday, and plan the vision task with vision planner
        
        Args:
            param1 (dict): task from Friday
        
        Returns:
            None
        '''
        
        plan_task_message = self.task_decompose_format_message(pre_task_info, task_name, task_description)
        
        # TESTCASE TEMP COMMENTED
        response = self.llm_provider.create_completion(plan_task_message, max_tokens=1000)
        self.logger.info(response)
        decomposed_tasks = self.extract_decomposed_tasks(response[0])
        
        # with open("testcase/decompose_task_message.json", "r") as f:
        #     decomposed_tasks = json.load(f)
        
        for _, task_info in decomposed_tasks.items():
            self.action_num += 1
            task_name = task_info['name']
            task_description = task_info['description']
            task_type = task_info['type']
            task_deatil = task_info['content']
            # task_dependencies = task_info['dependencies']
            self.vision_tasks.append(task_name)
            self.vision_nodes[task_name] = ActionNode(task_name, task_description, task_type, task_deatil)
    
    def task_decompose_format_message(self, pre_task_info, task_name, task_description):
        '''
            Send decompose task prompt to LLM and get task list.
            This compose of:
                1. pre_task_info
                2. current image information
                3. current task description with system prompt
        '''
        # system_prompt = self.templates.get("plan_task", "default")
        system_prompt = self.templates.get("decompose_system", "default")
        
        # user_prompt = self.templates.get("plan_task_user_prompt", "default")
        user_prompt = f"Please help me to decompose the task: {task_name}, {task_description}. If the current task is already completed, please still return json, but with a null dict."
        
        current_image = self.screen_helper.capture()
        current_image_base64 = current_image['base64']
        
        # user_prompt = self.prompt['_USER_TASK_REPLAN_PROMPT'].format(
        #     pre_task_info = pre_task_info,
        #     current_task_description = current_task_description,
        #     system_version=self.system_version,
        #     reasoning = reasoning,
        #     action_list = action_list,
        #     working_dir = self.environment.working_dir,
        #     files_and_folders = files_and_folders
        # )
        # current_image_base64 = 'fbase64'
        
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
                        "text": "previous task information: " + pre_task_info # 加入pre_task_info
                    },
                    {
                        "type": "text",
                        "text": "Current Screenshot:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": current_image_base64,    # 给出当前状态的截图
                            "detail": "low"
                        }
                    },
                    {
                        "type": "text",
                        "text": user_prompt # 给出我想要这一步做什么的task和描述
                    }
                ]
            },
        ]

        save_json(self.message, "decompose_task_message.json")
        return self.message

    def task_replan_format_message(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        # user_prompt = self.prompt['_USER_TASK_REPLAN_PROMPT'].format(
        #     current_task = current_task,
        #     current_task_description = current_task_description,
        #     system_version=self.system_version,
        #     reasoning = reasoning,
        #     action_list = action_list,
        #     working_dir = self.environment.working_dir,
        #     files_and_folders = files_and_folders
        # )
        pass
    
    def get_pre_tasks_info(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass
    
    def get_pre_tasks_info(self, current_task): # 传入的是action
        """
        Get string information of the prerequisite task for the current task.
        """
        pre_tasks_info = {}
        for task in self.vision_tasks:
            if task == current_task:
                break
            task_info = {
                "description" : self.vision_nodes[task].description,
                "return_val" : self.vision_nodes[task].return_val
            }
            pre_tasks_info[task] = task_info
        pre_tasks_info = json.dumps(pre_tasks_info)
        return pre_tasks_info
    
    def seeclick_task_planner(self, image_input: Union[str, Image.Image, None] = None, template_name: str = "seeclick_preprocess"):
        self.init_system_messages(template_name)
        base64_image = []
        
        if image_input is None:
            captured = self.screen_helper.capture()
            image_input = captured['image']
            base64_image.append(encode_single_data_to_base64(image_input))
        elif isinstance(image_input, str):
            base64_image.append(encode_single_data_to_base64(image_input))
        elif isinstance(image_input, Image.Image):
            base64_image.append(encode_single_data_to_base64(image_input))
        else:
            raise ValueError("Unsupported image input type.")
        
        screenshot_text = "Current Screenshot:"
        user_prompt = "What should I click on? Please use a short, comprehend sentence to describe the target. For example, 'Click on the red button.', 'Click on the image with a panda on it.'."
        
        self.messages.append({
            "role": "user",
            "content": [{
                "type": "text",
                "text": screenshot_text
            }, {
                "type": "image_url",
                "image_url": {
                    "url": base64_image[0]
                }
            }, {
                "type": "text",
                "text": user_prompt
            }]
        })
        
        return self.messages
        return self.llm_provider.create_completion(self.messages)
    
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

    def assemble_prompt(self, template_name: str, message_prompt: str, image_path: Union[str, List[str]]) -> str:
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} not found.")
        template: str = self.templates[template_name]

        encoded_images: List[str] = encode_data_to_base64_path(image_path)
        prompt: str = template.replace("{{message_prompt}}", message_prompt).replace("{{image_url}}", encoded_images[0])
        return prompt

    def append_images_to_message(self, message: Dict[str, Any], image_paths: Union[str, List[str]]) -> None:
        encoded_images: List[str] = encode_data_to_base64_path(image_paths)
        for encoded_image in encoded_images:
            msg_content: Dict[str, Any] = {
                "type": "image_url",
                "image_url": {"url": encoded_image}
            }
            message["content"].append(msg_content)

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
