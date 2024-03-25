from typing import Dict
from mss import mss
from PIL import Image
from utils.logger import Logger
import os
from datetime import datetime


class ScreenHelper:
    """
    ScreenHelper is a utility class for capturing screen shots,
    retrieving dimensions of the screen shots, and saving screen shots to files.

    Attributes:
        logger (Optional[logging.Logger]): An optional logger for logging operations.
        monitor (int): The index of the monitor to capture.
        sct (mss.mss): The MSS context for capturing the screen.
    """

    def __init__(self, logger: Logger = None, monitor: int = 1, path: str = "./working_dir/screenshot") -> None:
        """
        Initializes the ScreenHelper instance.

        Args:
            logger (Optional[logging.Logger]): An optional logger instance for logging.
            monitor (int): The index of the monitor to capture (1-based).
            path (str): The file path where the screenshot will be saved.
        """
        self.sct = mss()
        self.monitor = monitor
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.logger = logger
        if logger:
            self.logger.info(f"ScreenHelper initialized for monitor {monitor}")
    
    def capture(self, image_name: str = str(datetime.now().strftime("%Y%m%d_%H%M%S")) + '.png') -> list[Image.Image, Dict[str, int], str]:
        """
        Captures a screenshot of the specified monitor and returns it as a PIL Image.

        Returns:
            Image.Image: The captured screenshot as a PIL Image object.
        """
        
        captured = [self.capture_screenshot(), self.get_screenshot_dimensions()]
        if image_name:
            captured.append(self.save_image(image_name, captured[0]))

        if self.logger:
            self.logger.info("Screenshot captured")

        return captured

    def capture_screenshot(self) -> Image.Image:
        """
        Captures a screenshot of the specified monitor and returns it as a PIL Image.

        Returns:
            Image.Image: The captured screenshot as a PIL Image object.
        """
        monitor = self.sct.monitors[self.monitor]
        sct_img = self.sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        if self.logger:
            self.logger.info("Screenshot captured")

        return img

    def get_screenshot_dimensions(self) -> Dict[str, int]:
        """
        Retrieves the dimensions of the monitor specified for screen capture.

        Returns:
            Dict[str, int]: A dictionary containing the dimensions of the screen with keys 'left', 'top', 'width', 'height'.
        """
        monitor = self.sct.monitors[self.monitor]
        dimensions = {
            'left': monitor['left'],
            'top': monitor['top'],
            'width': monitor['width'],
            'height': monitor['height']
        }

        if self.logger:
            self.logger.info(f"Screenshot dimensions: {dimensions}")

        return dimensions

    def save_image(self, name: str, image: Image.Image = None) -> str:
        """
        Captures the current screen and saves the screenshot to a file.

        Args:
            path (str): The file path where the screenshot will be saved.
            image (Image.Image, optional): The image to save. If not provided, a new screenshot will be captured.
        """
        if image is None:
            image = self.capture_screenshot()
        file_path = os.path.join(self.path, name)
        image.save(file_path)

        if self.logger:
            self.logger.info(f"Screenshot saved to {file_path}")
        
        return file_path
    
    def show_image(self, img: Image.Image) -> None:
        """
        Displays the specified image in a window.

        Args:
            img (Image.Image): The image to display.
        """
        img.show()