from groundingdino.util.inference import load_model, load_image, predict, annotate
import torch
import os

WORKSPACE = os.getcwd()
GROUNDDINO_PATH = os.path.join(WORKSPACE, "GroundingDINO")
CONFIG_PATH = os.path.join(GROUNDDINO_PATH, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
WEIGHTS_NAME = "groundingdino_swint_ogc.pth" # groundingdino_swinb_cogcoor.pth
WEIGHTS_PATH = os.path.join(GROUNDDINO_PATH, "weights", WEIGHTS_NAME)
print(WEIGHTS_PATH, "; exist:", os.path.isfile(WEIGHTS_PATH))


device = "cuda" if torch.cuda.is_available() else "cpu"
model = load_model(CONFIG_PATH, WEIGHTS_PATH, device=device)

TEXT_PROMPT = "List"
BOX_TRESHOLD = 0.35
TEXT_TRESHOLD = 0.25

IMAGE_NAME = "test.png"
IMAGE_PATH = os.path.join(GROUNDDINO_PATH, IMAGE_NAME)
image_source, image = load_image(IMAGE_PATH)
image_source, image = load_image(IMAGE_PATH)

boxes, logits, phrases = predict(
    model=model, 
    image=image, 
    caption=TEXT_PROMPT, 
    box_threshold=BOX_TRESHOLD, 
    text_threshold=TEXT_TRESHOLD,
    device=device
)

print(boxes, logits, phrases)
annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)

# boxes (torch.Tensor): A tensor containing bounding box coordinates.
# logits (torch.Tensor): A tensor containing confidence scores for each bounding box.
# phrases (List[str]): A list of labels for each bounding box.