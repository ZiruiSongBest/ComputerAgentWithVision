from __future__ import annotations

import subprocess
import os
from friday.core.schema import EnvState
from friday.environment.env import Env
from tempfile import NamedTemporaryFile
from friday.action import get_os_version

class PythonEnv(Env):
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

    def step(self, _command: str, args: list[str] | str = []) -> EnvState:
        tmp_code_file = NamedTemporaryFile("w", dir=self.working_dir, suffix=".py", encoding="utf-8", delete=False)
        # Solving the issue of not being able to retrieve the current working directory of the last line of output
        _command = _command.strip() + "\n" + "import os" + "\n" + "print(os.getcwd())"
        tmp_code_file.write(_command)
        tmp_code_file.close()
        filename = tmp_code_file.name

        if isinstance(args, str):
            args = args.split()  # Convert space-separated string to a list

        self.env_state = EnvState(command=_command)

        try:
            if self.os_name == 'windows':
                # Get the path of the Python interpreter
                python_executable = os.path.join(os.environ['CONDA_PREFIX'], 'python.exe')
                env = os.environ.copy()
                env["PYTHONPATH"] = os.getcwd()
            else:
                python_executable = subprocess.run(["which", "python"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()
                env = {"PYTHONPATH": os.getcwd()}

            # Run the Python script
            results = subprocess.run(
                [python_executable, '-B', str(filename)] + args,
                encoding="utf8",
                check=True,
                cwd=self.working_dir,
                timeout=self.timeout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            # If there is standard output.
            if results.stdout:
                stout = results.stdout.strip().split('\n')
                self.env_state.result = "\n".join(stout[:-1])
                self.observe(stout[-1])
            return self.env_state
        except subprocess.CalledProcessError as e:
            self.env_state.error = e.stderr
        except Exception as e:
            self.env_state.error = repr(e)
        finally:
            os.unlink(filename)
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

DEFAULT_DESCRIPTION = """def solution():
    print("hello world!")
    print("hello world!")
    return "return!"
"""

if __name__ == '__main__':
    env = PythonEnv()
    print(env.step(DEFAULT_DESCRIPTION))
    # print(env.step("cd ../../"))
    # print(env.step("gogo"))
    # env.reset()
    # print(env.step("sleep 3")) # for macOS and Linux
    # print(env.step("timeout /t 3")) # for Windows