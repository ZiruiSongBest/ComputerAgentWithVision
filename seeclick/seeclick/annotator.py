import cv2
import numpy as np
import torch

class ImageAnnotator:
    def annotate(self, image_source: np.ndarray, boxes: torch.Tensor, draw_point: bool = False, annotate_color: tuple = (0, 255, 0)) -> np.ndarray:
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
