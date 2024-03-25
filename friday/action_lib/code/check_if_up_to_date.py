
from friday.action.base_action import BaseAction
import subprocess

class check_if_up_to_date(BaseAction):
    def __init__(self):
        self._description = "Execute a git command to check if the local branch is up to date with its corresponding remote branch."

    def __call__(self, directory_path, *args, **kwargs):
        """
        Executes a git command to check if the local branch is up to date with its corresponding remote branch in the specified directory.

        Args:
            directory_path (str): The path to the directory where the git command should be executed.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message indicating whether the local branch is up to date with the remote branch.
        """
        try:
            # Fetch the latest changes first to ensure the comparison is up to date
            subprocess.run(['git', '-C', directory_path, 'fetch'], check=True)
            # Check the status of the local branch in comparison to the remote branch
            result = subprocess.run(['git', '-C', directory_path, 'status', '-uno'], check=True, capture_output=True, text=True)
            if "Your branch is up to date" in result.stdout:
                print(f"The local branch in {directory_path} is up to date with its corresponding remote branch.")
            else:
                print(f"The local branch in {directory_path} is not up to date with its corresponding remote branch.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to check if the local branch is up to date in {directory_path}: {e}")

# Example of how to use the class (Do not directly copy this line into your code):
# check_if_up_to_date()('/Users/dylan/Desktop/1Res/osc/ComputerWithVisionMain')
