
from friday.action.base_action import BaseAction
import subprocess

class open_vscode(BaseAction):
    def __init__(self):
        self._description = "Execute a system command to open VSCode at a specified path."

    def __call__(self, path, *args, **kwargs):
        """
        Executes the system command to open VSCode at the specified path.

        Args:
            path (str): The path where VSCode should be opened.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the execution of the command.
        """
        try:
            subprocess.run(['open', '-a', 'Visual Studio Code', path], check=True)
            print(f"VSCode has been successfully opened at {path}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open VSCode at {path}: {e}")

# Example of how to use the class (Do not directly copy this line into your code):
# open_vscode()('/Users/dylan/Desktop/1Res/osc/ComputerWithVisionMain')
