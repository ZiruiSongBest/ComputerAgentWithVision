
from friday.action.base_action import BaseAction
import subprocess

class fetch_latest_changes(BaseAction):
    def __init__(self):
        self._description = "Execute a git command to fetch the latest changes from the remote repository for the specified directory."

    def __call__(self, directory_path, *args, **kwargs):
        """
        Executes a git command to fetch the latest changes from the remote repository for the specified directory.

        Args:
            directory_path (str): The path to the directory where the git command should be executed.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the execution of the fetch command.
        """
        try:
            subprocess.run(['git', '-C', directory_path, 'fetch'], check=True)
            print(f"Successfully fetched the latest changes for the repository in {directory_path}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch the latest changes for the repository in {directory_path}: {e}")
