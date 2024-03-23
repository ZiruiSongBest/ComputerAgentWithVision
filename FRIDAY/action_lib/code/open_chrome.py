
from friday.action.base_action import BaseAction
import subprocess

class open_chrome(BaseAction):
    def __init__(self):
        self._description = "Execute a system command to open Google Chrome on macOS."

    def __call__(self, *args, **kwargs):
        """
        Executes the system command to open Google Chrome on macOS.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the execution of the command.
        """
        try:
            subprocess.run(['open', '-a', 'Google Chrome'], check=True)
            print("Google Chrome has been successfully opened.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open Google Chrome: {e}")

# Example of how to use the class (Do not directly copy this line into your code):
# open_chrome()()
