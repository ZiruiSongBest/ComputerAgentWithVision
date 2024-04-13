import requests
import numpy as np
import cv2
import supervision as sv
import datetime
import torch
from typing import Union
from utils.screen_helper import ScreenHelper

class SeeClick:
    def __init__(self, screen_helper: ScreenHelper, url: str = 'http://100.119.14.85:8998/upload', prompt_template: str = "In this UI screenshot, what is the position of the element corresponding to the command \"{}\" (with point)?"):
        self.url = url
        self.prompt_template = prompt_template
        self.screen_helper = screen_helper

    def get_location(self, img_path: str, ref: str, custom_template: str = None) -> torch.Tensor:
        prompt = custom_template.format(ref) if custom_template else self.prompt_template.format(ref)
        files = {'image': open(img_path, 'rb')}
        data = {'text': prompt}

        response = requests.post(self.url, files=files, data=data).json()
        print(response['dot_location'])

        location = response['dot_location']
        return torch.tensor([[float(coord) for coord in location.strip("()").split(",")]])

    def get_location_with_current(self, ref: str, custom_template: str = None) -> torch.Tensor:
        captured = self.screen_helper.capture()
        files = {'image': open(captured['file_path'], 'rb')}
        data = {'text': ref}
        
        response = requests.post(self.url, files=files, data=data).json()
        print(response['dot_location'])
        location = response['dot_location']
        # location = "(0.39,0.48)"

        tensor_location = torch.tensor([[float(coord) for coord in location.strip("()").split(",")]])
        position = [captured['dimensions']['width'] * tensor_location[0][0], captured['dimensions']['height'] * tensor_location[0][1]] # 'left', 'top', 'width', 'height'
        
        captured.pop('base64')
        result = {
            "tensor": tensor_location,
            "position": position,
            "captured": captured
        }
        
        return result
    
    def annotate_image(self, image_source: Union[np.ndarray, str], boxes: torch.Tensor, draw_point: bool = True, annotate_color: tuple = (255, 0, 0)) -> np.ndarray:
        if isinstance(image_source, str):
            image_source = cv2.imread(image_source)

        h, w, _ = image_source.shape
        annotated_frame = cv2.cvtColor(image_source, cv2.COLOR_RGB2BGR)

        if boxes.dim() == 1:
            boxes = boxes.unsqueeze(0)

        if draw_point:
            for point in boxes:
                x, y = point.tolist()
                x, y = int(x * w), int(y * h)
                cv2.circle(annotated_frame, (x, y), radius=5, color=annotate_color, thickness=-1)
        else:
            for box in boxes:
                left, top, right, bottom = box.tolist()
                start_point = (int(left * w), int(top * h))
                end_point = (int(right * w), int(bottom * h))
                cv2.rectangle(annotated_frame, start_point, end_point, annotate_color, 2)

        return annotated_frame

    def save_annotated_image(self, annotated_frame: np.ndarray, save_path: str = '.', ref: str = 'annotated_image') -> str:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%m-%d_%H-%M")
        output_filename = "{}_{}_{}.png".format(ref.replace(" ", "_"), formatted_time, ref)
        output_path = "{}/{}".format(save_path.rstrip('/'), output_filename)

        cv2.imwrite(output_path, cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))
        return output_path

    def display_annotated_image(self, annotated_frame: np.ndarray):
        sv.plot_image(annotated_frame, (12, 7))


# if __name__ == '__main__':
    # from vision.grounding.seeclick import SeeClick
    # from utils.screen_helper import ScreenHelper

    # seeclick = SeeClick(ScreenHelper())


    # location = seeclick.get_location_with_current("search")

    # print(location['captured']['file_path'])

    # annotated_image = seeclick.annotate_image(location['captured']['file_path'], location['tensor'])
    # seeclick.save_annotated_image(annotated_image)
    # seeclick.display_annotated_image(annotated_image)