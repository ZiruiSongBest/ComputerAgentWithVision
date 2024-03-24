
from friday.action.base_action import BaseAction
import PyPDF2
import os

class extract_pdf_content(BaseAction):
    def __init__(self):
        self._description = "Extract the text content from the PDF file for further analysis."

    def __call__(self, pdf_file_path, working_dir=None, *args, **kwargs):
        """
        Extracts the text content from a specified PDF file located at a given path.

        Args:
            pdf_file_path (str): The path to the PDF file from which to extract text.
            working_dir (str, optional): The working directory where the PDF file is located. If not provided, uses the current working directory.

        Returns:
            str: The extracted text content from the PDF file.
        """
        # Set the working directory if provided
        if working_dir:
            os.chdir(working_dir)
        else:
            working_dir = os.getcwd()

        # Ensure the PDF file exists
        full_pdf_path = os.path.join(working_dir, pdf_file_path)
        if not os.path.exists(full_pdf_path):
            print(f"PDF file '{pdf_file_path}' does not exist in {working_dir}.")
            return

        try:
            # Open and read the PDF file
            with open(full_pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                text = ""
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            print("PDF content extracted successfully.")
            return text
        except Exception as e:
            print(f"Failed to extract content from the PDF file: {e}")

# Example of how to use the class (Do not directly copy this line into your code):
# extract_pdf_content()('/Users/dylan/Desktop/1Res/osc/ComputerAgentWithVision/working_dir/Job Listing.pdf', '/Users/dylan/Desktop/1Res/osc/ComputerAgentWithVision/working_dir')
