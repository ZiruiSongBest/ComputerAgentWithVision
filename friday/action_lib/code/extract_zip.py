
from friday.action.base_action import BaseAction
import zipfile
import os

class extract_zip(BaseAction):
    def __init__(self):
        self._description = "Extract the contents of a ZIP file to access specific files within."

    def __call__(self, zip_file_path, extract_to_folder, *args, **kwargs):
        """
        Extracts the contents of the specified ZIP file into a designated folder.

        Args:
            zip_file_path (str): The path to the ZIP file to be extracted.
            extract_to_folder (str): The folder where the contents of the ZIP file should be extracted.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the extraction of the ZIP file.
        """
        try:
            # Ensure the extraction folder exists
            if not os.path.exists(extract_to_folder):
                os.makedirs(extract_to_folder)
            
            # Extract the ZIP file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_folder)
            
            print(f"ZIP file extracted successfully to {extract_to_folder}")
        except Exception as e:
            print(f"Failed to extract the ZIP file: {e}")

# Example of how to use the class (Do not directly copy this line into your code):
# extract_zip()("/path/to/zip_file.zip", "/path/to/extract_to_folder")
