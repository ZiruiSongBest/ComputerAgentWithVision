
from friday.action.base_action import BaseAction
import subprocess

class check_current_branch(BaseAction):
    def __init__(self):
        self._description = "Execute a git command to check the current branch in the specified directory."

    def __call__(self, directory_path, *args, **kwargs):
        """
        Executes a git command to check the current branch in the specified directory.

        Args:
            directory_path (str): The path to the directory where the git command should be executed.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints the current git branch.
        """
        try:
            result = subprocess.run(['git', '-C', directory_path, 'branch', '--show-current'], check=True, capture_output=True, text=True)
            print(f"Current branch in {directory_path}: {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to check the current branch in {directory_path}: {e}")

# Example of how to use the class (Do not directly copy this line into your code):
# check_current_branch()('/Users/dylan/Desktop/1Res/osc/ComputerWithVisionMain')
