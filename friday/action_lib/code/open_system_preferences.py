
from friday.action.base_action import BaseAction
import subprocess

class open_system_preferences(BaseAction):
    def __init__(self):
        self._description = "Execute a system command to open System Preferences on macOS."

    def __call__(self, *args, **kwargs):
        """
        Executes the system command to open System Preferences on macOS.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the execution of the command.
        """
        try:
            # Attempt to open System Preferences using the correct path for macOS
            subprocess.run(['open', '-a', 'System Preferences'], check=True)
            print("System Preferences has been successfully opened.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open System Preferences: {e}")
        except Exception as e:
            # Handle unexpected errors
            print(f"An unexpected error occurred: {e}")
