import subprocess
import os
from friday.core.schema import EnvState
from friday.environment.env import Env
from friday.action import get_os_version

class BashEnv(Env):
    """Base class for all actions.

    Args:
        description (str, optional): The description of the action. Defaults to
            None.
        name (str, optional): The name of the action. If None, the name will
            be class name. Defaults to None.
    """

    def __init__(self) -> None:
        super().__init__()
        self._name: str = self.__class__.__name__
        self.os_name = get_os_version.get_os_name()

    def step(self, _command) -> EnvState:
        self.env_state = EnvState(command=_command)
        if self.os_name == 'windows':
            _command = _command() + ' & cd'
        else:
            _command = _command() + ' && pwd'

        try:
            results = subprocess.run(_command, capture_output=True, check=True, cwd=self.working_dir,
                                     text=True, shell=True, timeout=self.timeout)
            if results.stdout:
                stout = results.stdout.strip().split('\n')
                self.env_state.result = "\n".join(stout[:-1])
                self.observe(stout[-1])
            return self.env_state
        except subprocess.CalledProcessError as e:
            self.env_state.error = e.stderr
        except Exception as e:
            self.env_state.error = repr(e)
        self.observe(self.working_dir)
        return self.env_state

    def reset(self):
        self.working_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", "working_dir"))

    def observe(self, pwd):
        self.env_state.pwd = pwd
        self.working_dir = pwd
        if self.os_name == 'windows':
            self.env_state.ls = subprocess.run(['cmd.exe', '/c', 'dir'], cwd=self.working_dir, capture_output=True, text=True).stdout
        else:
            self.env_state.ls = subprocess.run(['ls'], cwd=self.working_dir, capture_output=True, text=True).stdout

if __name__ == '__main__':
    env = BashEnv()
    print(env.name)
    # print(env.step("ls")) # for macOS and Linux
    # print(env.step("dir")) # for Windows
    # print(env.step("cd ../../"))
    # print(env.step("gogo"))
    # env.reset()
    # print(env.step("sleep 3")) # for macOS and Linux
    # print(env.step("timeout /t 3")) # for Windows