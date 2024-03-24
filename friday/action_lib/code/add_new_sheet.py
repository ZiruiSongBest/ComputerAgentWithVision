
from friday.action.base_action import BaseAction
import openpyxl
import os

class add_new_sheet(BaseAction):
    def __init__(self):
        self._description = "Add a new sheet to an existing Excel file and name the new sheet as desired."

    def __call__(self, file_path, sheet_name, *args, **kwargs):
        """
        Adds a new sheet to the specified Excel file with the given sheet name.

        Args:
            file_path (str): The path to the Excel file where the new sheet will be added.
            sheet_name (str): The name of the new sheet to be added.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the addition of the new sheet.
        """
        # Ensure the Excel file exists
        if not os.path.exists(file_path):
            print(f"Excel file '{file_path}' does not exist.")
            return
        
        try:
            # Load the workbook and add a new sheet
            workbook = openpyxl.load_workbook(file_path)
            workbook.create_sheet(title=sheet_name)
            workbook.save(file_path)
            print(f"New sheet '{sheet_name}' has been successfully added to {file_path}.")
        except Exception as e:
            print(f"Failed to add new sheet '{sheet_name}' to {file_path}: {e}")
