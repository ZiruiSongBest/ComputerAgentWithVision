import requests
import numpy as np
import torch
from typing import Union, Dict
from utils.screen_helper import ScreenHelper

class OmniLMM:
    def __init__(self, screen_helper: ScreenHelper, url: str = 'http://localhost:8998/omni', prompt_template: str = "What text on the search box?"):
        self.url = url
        self.prompt_template = prompt_template
        self.screen_helper = screen_helper

    def get_response(self, ref: str, custom_template: Union[str, None] = None):
        try:
            captured = self.screen_helper.capture(heading=False)
            base64_img = captured['base64']
            # print(base64_img[:100])
            template = custom_template if custom_template else self.prompt_template
            data = {
                'content': ref,
                'image': base64_img
            }
            response = requests.post(self.url, data=data)
            print(response.text)

            if 'answer' not in response.json():
                raise ValueError("Response does not contain 'answer'")

            return response.json()['answer']

        except Exception as e:
            print(f"Error: {e}")
            return {"error": str(e)}

# Example Usage:
if __name__ == "__main__":
    screen_helper = ScreenHelper()
    omni_click = OmniLMM(screen_helper)
    print(omni_click.get_response("What is on the screen?"))
