from vision.grounding.seeclick import SeeClick
from utils.screen_helper import ScreenHelper
seeclick = SeeClick(ScreenHelper())

location = seeclick.get_location_with_current("search")

print(location)

annotated_image = seeclick.annotate_image(location['captured']['file_path'], location['tensor'])
seeclick.save_annotated_image(annotated_image)
seeclick.display_annotated_image(annotated_image)