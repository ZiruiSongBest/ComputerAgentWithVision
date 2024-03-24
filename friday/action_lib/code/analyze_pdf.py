
from friday.action.base_action import BaseAction
import PyPDF2
import os

class analyze_pdf(BaseAction):
    def __init__(self):
        self._description = "Analyze the content of the extracted PDF file to identify applicants and their qualifications."

    def __call__(self, pdf_file_path, working_dir=None, *args, **kwargs):
        """
        Analyzes the content of a PDF file to identify applicants and their qualifications.

        Args:
            pdf_file_path (str): The path to the PDF file to be analyzed.
            working_dir (str, optional): The working directory where the PDF file is located. If not provided, uses the current working directory.

        Returns:
            None, but prints the applicants and their qualifications found in the PDF file.
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
                
                # Analyze the text for applicants and their qualifications
                # This is a placeholder for the analysis logic
                # You should replace this with actual analysis code
                print("Applicants and their qualifications found in the PDF:")
                print(text)  # Placeholder for actual analysis output
        except Exception as e:
            print(f"Failed to analyze the PDF file: {e}")
