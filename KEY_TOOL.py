from typing import (
    Any,
    Dict,
    List,
    Tuple,
)
import os
import time
import ctypes #可以直接调用C函数

from ahk import AHK
import pydirectinput

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure): #表示键盘输入
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]

class HardwareInput(ctypes.Structure): #表示硬件输入
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]


class MouseInput(ctypes.Structure): #表示鼠标输入
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)] #一个联合体，让三种操作共享内存空间


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)] #根据type的值指定是哪种输入


class IOEnvironment():
    """
    Wrapper for resources to interact with the game to make sure they're available where needed and multiple instances are not created.
    """

    # Windows API constants
    MOUSEEVENTF_MOVE = 0x0001 #鼠标移动事件标识
    MOUSEEVENTF_ABSOLUT = 0x8000 #绝对坐标
    WIN_NORM_MAX = 65536 # windows窗口的最大值

    def __init__(self) -> None:
        """Initialize the IO environment class"""
        self.ahk = AHK() #AHK也是用来模拟键盘输入输出
        pydirectinput.FAILSAFE = False

    def mouse_move(self, x, y, relative=False): #
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()

        event_flag = self.MOUSEEVENTF_MOVE

        if relative is False:
            event_flag = self.MOUSEEVENTF_ABSOLUT | self.MOUSEEVENTF_MOVE

        ii_.mi = MouseInput(int(x), int(y), 0, event_flag, 0, ctypes.pointer(extra))

        command = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

    def mouse_click(self, button, duration = None, clicks=1): #鼠标点击
        self.mouse_click_button(button, duration, clicks)

    def mouse_click_button(self, button, clicks=1):
        button = self.map_button(button)
        self.ahk.click(click_count=clicks, button=button, relative=False)


    def get_mouse_position(self) -> Tuple[int, int]:
        return self.ahk.get_mouse_position()

    def _check_multi_key(self, input): #检查输入是否为多个按键组合

        if input is not None and len(input) > 1:
            if type(input) is list:
                return (True, input)
            else:
                key_tokens = input.split(',')
                keys = []
                for k in key_tokens:
                    k = k.strip()
                    if k != '':
                        k = self.map_key(k)
                        keys.append(k)

                if len(keys) == 0:
                    return (False, None)
                elif len(keys) == 1:
                    return (False, keys[0])
                else:
                    return (True, keys)

        else:
            return (False, None)

    def _multi_key_action(self, keys, duration = 2):

        # Act in order, release in reverse
        for key in keys:
            self.key_press(key)
        
        if duration is None:
            duration = 0.3

        time.sleep(duration)


    def key_press(self, key):

        if key in self.ALIASES_MOUSE_REDIRECT:
            self.mouse_click_button(key)

        key = self.map_key(key)

        f, keys = self._check_multi_key(key)
        if f == True:
            self._multi_key_action(keys, self.ACTION_PRESS)
        else:
            pydirectinput.keyDown(key)
            time.sleep(.2)
            pydirectinput.keyUp(key)


    ALIASES_RIGHT_MOUSE = ['right', 'rightbutton', 'rightmousebutton', 'r', 'rbutton', 'rmouse', 'rightmouse', 'rm', 'mouseright', 'mouserightbutton']
    ALIASES_LEFT_MOUSE = ['left', 'leftbutton', 'leftmousebutton', 'l', 'lbutton', 'lmouse', 'leftmouse', 'lm', 'mouseleft', 'mouseleftbutton']
    ALIASES_CENTER_MOUSE = ['middle', 'middelbutton', 'middlemousebutton', 'm', 'mbutton', 'mmouse', 'middlemouse', 'center', 'c', 'centerbutton', 'centermouse', 'cm', 'mousecenter', 'mousecenterbutton']
    ALIASES_MOUSE_REDIRECT = set(ALIASES_RIGHT_MOUSE + ALIASES_LEFT_MOUSE + ALIASES_CENTER_MOUSE) - set(['r', 'l', 'm', 'c'])

    # @TODO mapping can be improved
    def map_button(self, button):

        if button is None or button == '':
            raise Exception(f'Empty mouse button IO: {button}')

        if len(button) > 1:
            button = button.lower().replace('_', '').replace(' ', '')

        if button in self.ALIASES_RIGHT_MOUSE:
            return self.RIGHT_MOUSE_BUTTON
        elif button in self.ALIASES_LEFT_MOUSE:
            return self.LEFT_MOUSE_BUTTON
        elif button in self.ALIASES_CENTER_MOUSE:
            return self.MIDDLE_MOUSE_BUTTON

        return button

    ALIASES_RIGHT_SHIFT_KEY = ['rshift', 'right shift', 'rightshift', 'shift right', 'shiftright']
    ALIASES_LEFT_SHIFT_KEY = ['lshift', 'left shift', 'leftshift', 'shift left', 'shiftleft']
    ALIASES_SHIFT_KEY = ALIASES_RIGHT_SHIFT_KEY + ALIASES_LEFT_SHIFT_KEY

    ALIASES_RIGHT_ALT_KEY = ['ralt', 'right alt', 'rightalt', 'alt right', 'altright']
    ALIASES_LEFT_ALT_KEY = ['lalt', 'left alt', 'leftalt', 'alt left', 'altleft']
    ALIASES_ALT_KEY = ALIASES_RIGHT_ALT_KEY + ALIASES_LEFT_ALT_KEY

    ALIASES_RIGHT_CONTROL_KEY = ['rctrl', 'right ctrl', 'rightctrl', 'ctrl right', 'ctrlright', 'rcontrol', 'right control', 'rightcontrol', 'control right', 'contorlright']
    ALIASES_LEFT_CONTROL_KEY = ['lctrl', 'left ctrl', 'leftctrl', 'ctrl left', 'ctrlleft', 'lcontrol', 'left control', 'leftcontrol', 'control left', 'contorlleft']
    ALIASES_CONTROL_KEY = ALIASES_RIGHT_CONTROL_KEY + ALIASES_LEFT_CONTROL_KEY

    ALIASES_SPACE_KEY = [' ', 'whitespace', 'spacebar', 'space bar']

    # @TODO mapping can be improved
    def map_key(self, key):

        if key is None or key == '':
            raise Exception(f'Empty key IO: {key}')

        if len(key) > 1:
            key = key.lower().replace('_', '').replace('-', '')
        elif len(key) == 1:
            key = key.lower()

        if key in self.ALIASES_LEFT_SHIFT_KEY:
            return 'shift'
        elif key in self.ALIASES_RIGHT_SHIFT_KEY:
            return 'shift'

        if key in self.ALIASES_LEFT_ALT_KEY:
            return 'alt'
        elif key in self.ALIASES_RIGHT_ALT_KEY:
            return 'alt'

        if key in self.ALIASES_LEFT_CONTROL_KEY:
            return 'ctrl'
        elif key in self.ALIASES_RIGHT_CONTROL_KEY:
            return 'ctrl'

        if key in self.ALIASES_SPACE_KEY:
            return 'space'
        
        return key
#prompt for 
""" 
    Action_guidance: I will give guidance on how to perform a task using keyboard keys or mouse buttons; you must generate the code based on the on-screen text. The content of the code should obey the following code rules:
    1. You should first identify the exact keyboard or mouse key represented by the icon on the screenshot. 'Ent' refers to 'enter'. 'RM' refers to 'right mouse button'. 'LM' refers to 'left mouse button'. You should output the full name of the key in the code.
    2. You should refer to different examples strictly based on the word used to control the key, such as 'use', 'hold', 'release', 'press', and 'click'.
    3. If 'use' or 'press' is in the prompt to control the keyboard key or mouse button, io_env.key_press('key', 2) or io_env.mouse_press('button', 2) must be used to act on it. Refer to Examples 1, 2, and 3.
    4. If there are multiple keys, io_env.key_press('key1,key2', 2) must be used to act on it. Refer to Example 4.
    5. If 'hold' is in the prompt to control the keyboard key or mouse button, it means keeping the key held with io_env.key_hold or the button held with io_env.mouse_hold (usually indefinitely, with no duration). If you need to hold it briefly, specify a duration argument. Refer to Examples 5 and 6.
    6. All durations are set to a minimum of 2 seconds by default. You can choose a longer or shorter duration. If it should be indefinite, do not specify a duration argument.
    7. The name of the created function should only use phrasal verbs, verbs, nouns, or adverbs shown in the prompt and should be in the verb+noun or verb+adverb format, such as drink_water, slow_down_car, and ride_faster. Note that words that do not show in the prompt are prohibited.

    This is Example 1. If "press" is in the prompt and the text prompt on the screenshot is "press X to play the card", your output should be:
    ```python
    def play_card():
        \"\"\"
        press "x" to play the card
        \"\"\"
        io_env.key_press('x', 2)
    '''
    This is Example 2. If the instructions involve the mouse and the text prompt on the screenshot is "use the left mouse button to confirm", your output should be:
    ```python
    def confirm():
        \"\"\"
        use "left mouse button" to confirm
        \"\"\"
        io_env.mouse_press("left mouse button")
    ```
    This is Example 3. If "use" is in the prompt and the text prompt on the screenshot is "use ENTER to drink water", your output should be:
    ```python
    def drink_water():
        \"\"\"
        use "enter" to drink water
        \"\"\"
        io_env.key_press('enter', 2)
    ```
    This is Example 4. If "use" is in the prompt and the text prompt on the screenshot is "use W and J to jump the barrier", your output should be:
    ```python
    def jump_barrier():
        \"\"\"
        use "w" and "j" to jump the barrier
        \"\"\"
        io_env.key_press('w,j', 3)
    ```
    This is Example 5. If "hold" is in the prompt and the text prompt on the screenshot is "hold H to run", your output should be:
    ```python
    def run():
        \"\"\"
        hold "h" to run
        \"\"\"
        io_env.key_hold('h')
    ```
    This is Example 6. If the instructions involve the mouse and the text prompt on the screenshot is "hold the right mouse button to focus on the target", your output should be:
    ```python
    def focus_on_target():
        \"\"\"
        hold "right mouse button" to focus
        \"\"\"
        io_env.mouse_hold("right mouse button")
    ```
    This is Example 7. If "release" is in the prompt and the text prompt on the screenshot is "release Q to drop the items", your output should be:
    ```python
    def drop_items():
        \"\"\"
        release "q" to drop the items
        \"\"\"
        io_env.key_release('q')
    ```

    I want to shut down the web
"""

