from friday.action.base_action import BaseAction
import subprocess
from friday.environment.py_env import PythonEnv

class execute_system_command(BaseAction):
    def __init__(self):
        self._description = "Executes a specified system command."

    def __call__(self, command, *args, **kwargs):
        """
        Executes a given system command using the subprocess module.

        Args:
            command (str): The system command to be executed.
            *args: Additional arguments for the command (optional).
            **kwargs: Additional keyword arguments for subprocess.run (optional).

        Returns:
            subprocess.CompletedProcess: The result of the executed command.
        """
        try:
            result = subprocess.run([command] + list(args), **kwargs, capture_output=True, text=True)
            print(f"Command '{command}' executed successfully.")
            return result
        except Exception as e:
            print(f"Error executing command '{command}': {e}")
            return None

from friday.environment.env import Env
pythonenv = PythonEnv()

commands = '''from friday.action.base_action import BaseAction
import subprocess

class open_notepad(BaseAction):
    def __init__(self):
        self._description = "Execute a system command to open Notepad on Windows."

    def __call__(self, *args, **kwargs):
        """
        Opens Notepad application on Windows.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None. Opens Notepad application.
        """
        try:
            subprocess.run("notepad.exe", check=True)
            print("Notepad opened successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open Notepad: {e}")

# Example of how to use the class
# Note: This is just an example and should not be executed in this script.
# open_notepad()()

result=open_notepad()()
print("<return>")
print(result)
print("</return>")'''

print(pythonenv.step(commands, []))