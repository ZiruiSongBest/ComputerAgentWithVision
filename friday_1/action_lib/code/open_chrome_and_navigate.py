
from friday.action.base_action import BaseAction
import subprocess

class open_chrome_and_navigate(BaseAction):
    def __init__(self):
        self._description = "Execute a system command to open Google Chrome on macOS and navigate to a specified URL."

    def __call__(self, url="http://youtube.com", *args, **kwargs):
        """
        Executes the system command to open Google Chrome on macOS and navigates to the specified URL.

        Args:
            url (str): The URL to navigate to. Defaults to "http://youtube.com".
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the execution of the command.
        """
        try:
            subprocess.run(['open', '-a', 'Google Chrome', url], check=True)
            print(f"Google Chrome has been successfully opened and navigated to {url}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open Google Chrome and navigate to {url}: {e}")
