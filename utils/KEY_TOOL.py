import os
import time
import pyautogui


class IOEnvironment():
    """
    Wrapper for resources to interact with the game to make sure they're available where needed and multiple instances are not created.
    """

    MOUSEEVENTF_MOVE = 0x0001 #鼠标移动事件标识
    MOUSEEVENTF_ABSOLUT = 0x8000 #绝对坐标
    WIN_NORM_MAX = 65536 # windows窗口的最大值

    def mouse_move(self, x, y):
        pyautogui.moveTo(x, y, duration=0.2)  # 同样，duration参数可使移动更平滑


    def mouse_click(self, button='left', clicks=1, interval=0.0, duration=None):
        """
        使用PyAutoGUI执行鼠标点击。

        参数:
        - button: 点击的按钮，可以是'left' 'middle' 'right'。
        - clicks: 点击次数 默认为1。
        - interval: 两次点击之间的间隔时间 单位为秒。
        """
        # 执行点击操作
        pyautogui.click(clicks=clicks, interval=interval, button=button)

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

        key = self.map_key(key)

        f, keys = self._check_multi_key(key)
        if f == True:
            self._multi_key_action(keys, self.ACTION_PRESS)
        else:
            pyautogui.keyDown(key)
            time.sleep(.2)
            pyautogui.keyUp(key)


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
    
# I = IOEnvironment()
# I.mouse_move(900,700)
# I.mouse_click('left',1,0,0)
# I.key_press("A")