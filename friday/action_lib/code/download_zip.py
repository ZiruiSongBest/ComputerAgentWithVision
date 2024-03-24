
from friday.action.base_action import BaseAction
import requests
import os

class download_zip(BaseAction):
    def __init__(self):
        self._description = "Download a ZIP file from a specified URL to the local system."

    def __call__(self, url, destination_folder, *args, **kwargs):
        """
        Downloads a ZIP file from the specified URL and saves it to the destination folder.

        Args:
            url (str): The URL from which to download the ZIP file.
            destination_folder (str): The local folder where the ZIP file should be saved.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None, but prints a message confirming the download and location of the ZIP file.
        """
        try:
            # Ensure the destination folder exists
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            # Extract the file name from the URL
            file_name = url.split('/')[-1]
            destination_path = os.path.join(destination_folder, file_name)
            
            # Download the file
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
            
            # Save the file
            with open(destination_path, 'wb') as f:
                f.write(response.content)
            
            print(f"ZIP file downloaded successfully and saved to {destination_path}")
        except Exception as e:
            print(f"Failed to download the ZIP file: {e}")

# Example of how to use the class (Do not directly copy this line into your code):
# download_zip()("https://example.com/file.zip", "/path/to/destination")
