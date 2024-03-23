from collections import namedtuple
import os
import time
from pathlib import Path

from dotenv import load_dotenv
import pyautogui

from utils import Singleton
from utils.file_utils import assemble_project_path, get_project_root

load_dotenv(verbose=True)


class Config(metaclass=Singleton):
    """
    Configuration class.
    """

    # DEFAULT_GAME_RESOLUTION = (1920, 1080)
    # DEFAULT_GAME_SCREEN_RATIO = (16, 9)

    DEFAULT_TEMPERATURE = 1.0
    DEFAULT_SEED = None

    DEFAULT_FIXED_SEED_VALUE = 42
    DEFAULT_FIXED_TEMPERATURE_VALUE = 0.0

    # DEFAULT_POST_ACTION_WAIT_TIME = 3 # Currently in use in multiple places with this value

    root_dir = '.'
    work_dir = './runs'
    log_dir = './logs'

    def __init__(self) -> None:
        """Initialize the Config class"""

        self.debug_mode = False
        self.continuous_mode = False
        self.continuous_limit = 0

        self.temperature = self.DEFAULT_TEMPERATURE
        self.seed = self.DEFAULT_SEED
        self.fixed_seed = False

        if self.fixed_seed:
            self.set_fixed_seed()

        self.base_resolution = (3840, 2160)

        self.screen_resolution = pyautogui.size()
        self.mouse_move_factor = self.screen_resolution[0] / self.base_resolution[0]

        # Default LLM parameters
        self.temperature = float(os.getenv("TEMPERATURE", self.temperature))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1024"))

        #Skill retrieval
        self.skill_from_local = True
        self.skill_local_path = './res/skills'
        self.skill_retrieval = False
        self.skill_num = 10
        self.skill_scope = 'Full' #'Full', 'Basic', and None

        # self-reflection
        self.max_images_in_self_reflection = 4

        # decision-making
        self.decision_making_image_num = 2


        # Just for convenience of testing, will be removed in final version.
        self.use_latest_memory_path = False
        if self.use_latest_memory_path:
            self._set_latest_memory_path()

        self._set_dirs()
        self._set_game_window_info()


    def set_fixed_seed(self, is_fixed: bool = True, seed: int = DEFAULT_FIXED_SEED_VALUE, temperature: float = DEFAULT_FIXED_TEMPERATURE_VALUE) -> None:
        """Set the fixed seed values. By default, used the default values. Please avoid using different values."""
        self.fixed_seed = is_fixed
        self.seed = seed
        self.temperature = temperature


    def set_continuous_mode(self, value: bool) -> None:
        """Set the continuous mode value."""
        self.continuous_mode = value


    def _set_dirs(self) -> None:
        """Setup directories needed for one system run."""
        self.root_dir = get_project_root()

        self.work_dir = assemble_project_path(os.path.join(self.work_dir, str(time.time())))
        Path(self.work_dir).mkdir(parents=True, exist_ok=True)

        self.log_dir = os.path.join(self.work_dir, self.log_dir)
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)