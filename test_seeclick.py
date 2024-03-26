from vision.grounding.seeclick import SeeClick
import json

seeclick = SeeClick()

# img = '/Users/dylan/Downloads/Snipaste_2024-03-26_19-53-12.png'
# desc = "Search Google or type a URL"
# location = seeclick.get_location(img, desc)
# annotated = seeclick.annotate_image(img, location)
# seeclick.save_annotated_image(annotated, ref='google')


img = "/Users/dylan/Downloads/Snipaste_2024-03-26_19-54-39.png"
desc = "Friends Series"
desc = "The content below Search Google or type a URL"
location = seeclick.get_location(img, desc)
annotated = seeclick.annotate_image(img, location)
seeclick.save_annotated_image(annotated, ref='googlesearch')