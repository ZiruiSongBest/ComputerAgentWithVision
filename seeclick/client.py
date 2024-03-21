import requests
import numpy as np
import cv2
import supervision as sv
import datetime
import torch

def annotate(image_source: np.ndarray, boxes: torch.Tensor, draw_point: bool = False, annotate_color: tuple = (0, 255, 0)) -> np.ndarray:
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
        # Iterate over bounding boxes
        for box in boxes:
            left, top, right, bottom = box.tolist()
            start_point = (int(left * w), int(top * h))
            end_point = (int(right * w), int(bottom * h))
            cv2.rectangle(annotated_frame, start_point, end_point, annotate_color, 2)

    return annotated_frame


img_path = '/Users/dylan/Downloads/Snipaste_2024-03-06_15-19-25.png'
ref = 'play button'

url = 'http://100.119.14.85:8998/upload'
files = {'image': open(img_path, 'rb')}
data = {'text': ref}

response = requests.post(url, files=files, data=data).json()
print(response['dot_location'])

location = response['dot_location']
boxes = torch.tensor([[float(coord) for coord in location.strip("()").split(",")]])
annotated_frame = annotate(image_source=img_path, boxes=boxes, draw_point=True, annotate_color=(0, 0, 255))
sv.plot_image(annotated_frame, (12, 7))

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

output_path = "./{}_{}_{}.png".format(ref.replace(" ", "_"), formatted_time, ref)

cv2.imwrite(output_path, cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))