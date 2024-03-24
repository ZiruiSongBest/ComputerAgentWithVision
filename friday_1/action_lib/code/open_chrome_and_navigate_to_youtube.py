
from friday.action.base_action import BaseAction
import subprocess

class open_chrome_and_navigate_to_youtube(BaseAction):
    def __init__(self):
        self._description = "Execute a system command to open Google Chrome on macOS and navigate to youtube.com."

    def __call__(self, *args, **kwargs):
        """
        Executes the system command to open Google Chrome on macOS and navigates to youtube.com.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the execution of the command.
        """
        url = "http://youtube.com"
        try:
            subprocess.run(['open', '-a', 'Google Chrome', url], check=True)
            print(f"Google Chrome has been successfully opened and navigated to {url}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open Google Chrome and navigate to {url}: {e}")
