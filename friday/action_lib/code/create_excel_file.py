
from friday.action.base_action import BaseAction
import xlsxwriter
import os

class create_excel_file(BaseAction):
    def __init__(self):
        self._description = "Create a new Excel file in the specified directory with a given name."

    def __call__(self, directory, file_name, *args, **kwargs):
        """
        Creates a new Excel file in the specified directory with the given file name.

        Args:
            directory (str): The directory where the Excel file will be created.
            file_name (str): The name of the Excel file to be created, including the .xlsx extension.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the creation of the Excel file.
        """
        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Change the current working directory to the specified directory
        os.chdir(directory)
        
        # Create the Excel file
        try:
            workbook = xlsxwriter.Workbook(file_name)
            workbook.close()
            print(f"Excel file '{file_name}' has been successfully created in {directory}.")
        except Exception as e:
            print(f"Failed to create Excel file '{file_name}' in {directory}: {e}")
