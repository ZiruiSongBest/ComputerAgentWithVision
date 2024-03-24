
from friday.action.base_action import BaseAction
import re

class analyze_pdf_content(BaseAction):
    def __init__(self):
        self._description = "Analyze the extracted text content to identify applicants and their qualifications, and determine which applicants are missing a single qualification."

    def __call__(self, extracted_text, *args, **kwargs):
        """
        Analyzes the extracted text content from a PDF to identify applicants, their qualifications, and those missing only a single qualification.

        Args:
            extracted_text (str): The text content extracted from the PDF file.

        Returns:
            list: A list of applicants missing only a single qualification.
        """
        # Split the text into lines for processing
        lines = extracted_text.split('\n')
        
        # Placeholder for applicants and their qualifications
        applicants = {}
        
        # Placeholder for applicants missing a single qualification
        applicants_missing_one_qualification = []
        
        # Regex pattern to identify applicant names and qualifications
        applicant_pattern = re.compile(r'^Name: (.+)$')
        qualification_pattern = re.compile(r'^Qualifications: (.+)$')
        
        current_applicant = None
        
        for line in lines:
            # Check for applicant name
            name_match = applicant_pattern.match(line)
            if name_match:
                current_applicant = name_match.group(1)
                applicants[current_applicant] = []
                continue
            
            # Check for qualifications
            qualification_match = qualification_pattern.match(line)
            if qualification_match and current_applicant:
                qualifications = qualification_match.group(1).split(', ')
                applicants[current_applicant].extend(qualifications)
        
        # Determine which applicants are missing a single qualification
        for applicant, qualifications in applicants.items():
            if len(qualifications) == 1:
                applicants_missing_one_qualification.append(applicant)
        
        # Print the result
        print("Applicants missing only a single qualification:", applicants_missing_one_qualification)
        
        return applicants_missing_one_qualification
