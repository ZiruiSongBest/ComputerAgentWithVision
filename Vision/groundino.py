# import necessary modules at the beginning of the file
from groundingdino.util.inference import load_model, load_image, predict, annotate
import torch
import os
import cv2

def process_image(image_name, text_prompt, box_threshold=0.35, text_threshold=0.25):
    # Set up paths and constants
    workspace = os.getcwd()
    grounddino_path = os.path.join(workspace, "GroundingDINO")
    config_path = os.path.join(grounddino_path, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
    weights_name = "groundingdino_swint_ogc.pth"  # You can change this to another weights file if needed
    weights_path = os.path.join(grounddino_path, "weights", weights_name)
    
    # Check if weights file exists
    if not os.path.isfile(weights_path):
        print(f"Weights file does not exist at {weights_path}")
        return

    # Initialize the device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load the model
    model = load_model(config_path, weights_path, device=device)
    
    # Load the image
    image_path = os.path.join(grounddino_path, image_name)
    image_source, image = load_image(image_path)
    
    # Make predictions
    boxes, logits, phrases = predict(
        model=model, 
        image=image, 
        caption=text_prompt, 
        box_threshold=box_threshold, 
        text_threshold=text_threshold,
        device=device
    )

    # Annotate the image
    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    
    # Save the annotated image
    annotated_image_path = os.path.join(workspace, "annotated_" + image_name)
    annotated_frame_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
    cv2.imwrite(annotated_image_path, annotated_frame_bgr)

    print(f"Annotated image saved at {annotated_image_path}")
    return annotated_image_path

# Now you can call this function from another file like so:
# from your_script_name import process_image
# annotated_im age_path = process_image("cartoon.jpeg", "chair")
