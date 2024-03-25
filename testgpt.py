from vision.core.vision import VisionExecutor
from utils.logger import Logger
from vision.grounding.seeclick import SeeClick
import json

visionExecutor = VisionExecutor()

if __name__ == "__main__":
    
    logger = Logger()

    visionExecutor = VisionExecutor()
    data = json.dumps(visionExecutor.seeclick_task_planner(), indent=4)
    print(data)
    
# seeclick = SeeClick()
# seeclick.get_location("screenshot.png", "sign up")