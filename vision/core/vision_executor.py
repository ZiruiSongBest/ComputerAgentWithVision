import json
from typing import List, Dict, Any

import torch
from vision.llm.openai import OpenAIProvider
from vision.grounding.seeclick import SeeClick
from vision.grounding.omnilmm import OmniLMM
from utils.encode_image import encode_data_to_base64_path, encode_single_data_to_base64
from utils.screen_helper import ScreenHelper
from utils.KEY_TOOL import IOEnvironment
from utils.logger import Logger
from vision.prompt.prompt import prompt

'''
1. 读取task, 并且执行操作
2. 检查task是否完成
返回结果

1. entertext: 输入一系列文本
2. click: 点击某个位置
3. click_and_enter: 点击某个位置，然后输入一系列文本
4. scroll
# 3. drag: 拖拽某个位置
# 4. select: 选择某个位置
# 5. wait: 等待一段时间


包含调用系统KEY_TOOL的各种操作, 还有键入等
'''
class VisionExecutor:
    def __init__(self, template_file_path: str = None, llm_provider: OpenAIProvider = None, seeclick: SeeClick = None, omnilmm: OmniLMM = None, screen_helper: ScreenHelper = None, key_tool: IOEnvironment = None, system_version: str = None, logger: Logger = None) -> None:
        # Helpers
        self.llm_provider = llm_provider
        self.seeclick = seeclick
        self.omnilmm = omnilmm
        self.screen_helper = screen_helper
        self.key_tool = key_tool
        self.logger = logger
        
        # templates
        self.templates: Dict[str, str] = {}
        self._init_templates(template_file_path)
        
        # variables
        self.messages: List[Dict[str, Any]] = []
        self.system_version = system_version
        self.vision_tasks = []
    
    def _init_templates(self, template_file_path) -> None:
        if template_file_path:
            with open(template_file_path, 'r') as f:
                self.templates = json.load(f)
        else:
            self.templates = prompt
    
    
    def measure_execution(self, task, images) -> str:
        """measure

        Args:
            task (str): the task to be executed
            images ([str]): two base64 images

        Returns:
            [bool, str]: the response of the result. If the task is completed, return True, else return False and the reason
        """
        self.messages.append({
            "role": "user",
            "content": [{
                "type": "text",
                "text": prompt["Judge"] + task
            }, {
                "type": "image_url",
                "image_url": {
                    "url": images[0]
                },
                "description" : "The image before operation"
            }, {
                "type": "image_url",
                "image_url": {
                    "url": images[1]
                },
                "description" : "The image after operation"
            }]
        })
        [message, info] = self.llm_provider.create_completion(self.messages)
        if message == "FINISH":
            return [True,None]
        else:
            return [False,message]

    def text_regularization(self, text):
        result = []
        i = 0
        in_tag = False  
        tag_start = 0  
        s = text
        while i < len(s):
            if s[i] == "<" and not in_tag and (i == 0 or s[i-1] != "\\"):
                in_tag = True
                tag_start = i
            elif s[i] == ">" and in_tag: 
                in_tag = False
                result.append(s[tag_start+1:i])
            elif not in_tag:
                if s[i] == " ": 
                    result.append("space")
                else:  
                    result.append(s[i])
            i += 1

        return result
    
    def enter(self, text):
        text_list = self.text_regularization(text)
        self.logger.info(f"Enter text: {text_list}")
        for key in text_list:
            self.key_tool.key_press(key)
        return 'success'
    
    def click(self, content):
        image_before = self.screen_helper.capture(heading=False)['base64']
        result = self.seeclick.get_location_with_current(content)
        x, y = result['position'][0].item(), result['position'][1].item()
        
        self.key_tool.move_and_click(x, y, button='left', clicks=2, interval=2, duration=None)
        
        if not self.assess(content, image_before):
            return 'success'
        return 'fail'
    
    def observe(self, content):
        captured = self.screen_helper.capture()
        current_screen = encode_single_data_to_base64(captured['image'])
        self.messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": content
                }, 
                {
                    "type": "image_url",
                    "image_url": {
                        "url": current_screen
                    }
                }
            ]
        })
        response = self.llm_provider.create_completion(self.messages)
        self.logger.info(response)
        return response[0]

    def assess(self, content, image_before):
        measure_prompt = f"Please judge whether the operation is successful, answer in yes and failure {content}. Don't answer failure if you are not sure."
        response = self.omnilmm.get_response(measure_prompt)
        self.logger.info(response)
        if not 'failure' in response:
            return True
        return False
# shape = VisionExecutor()
# shape.enter_text("ABCDEFG")