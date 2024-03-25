from typing import List, Dict, Union, Any
from vision.llm.openai import OpenAIProvider
from vision.grounding.seeclick import SeeClick
from utils.encode_image import encode_data_to_base64_path, encode_single_data_to_base64
from utils.screen_helper import ScreenHelper
from utils.KEY_TOOL import IOEnvironment
from utils.logger import Logger


'''
1. 读取task, 并且执行操作
2. 检查task是否完成
返回结果

1. entertext: 输入一系列文本
2. click: 点击某个位置
3. click_and_enter: 点击某个位置，然后输入一系列文本
# 3. keyboard: 键盘组合键
# 3. drag: 拖拽某个位置
# 4. select: 选择某个位置
# 5. wait: 等待一段时间


包含调用系统KEY_TOOL的各种操作, 还有键入等
'''
class Vision_Executor:
    def __init__(self, template_file_path: str = None, llm_provider: OpenAIProvider = None, seeclick: SeeClick = None, screen_helper: ScreenHelper = None, key_tool: IOEnvironment = None, system_version: str = None, logger: Logger = None) -> None:
        # Helpers
        self.llm_provider = llm_provider
        self.seeclick = seeclick
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

    def execute(self, task):
        self.logging.debug("The current task is: {task}".format(task=task.description))
        if task.type == "click":
            click_x, click_y = []
            self.key_tool.move_and_click(click_x, click_y)
        elif task.type == "click and Enter":
            click_x, click_y = []
            text = ""
            self.key_tool.move_and_click(click_x, click_y)
            self.key_tool.enter_text(text)
        elif task.type == "scroll":
            scroll_type, scroll_times = []
            self.key_tool.scroll(scroll_type, scroll_times)
        elif task.type == "keyboard":
            self.key_tool.key_press(text)