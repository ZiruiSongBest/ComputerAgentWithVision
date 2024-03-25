import base64
import os
from typing import List, Any
from PIL import Image
import numpy as np
import io
import cv2

def encode_base64(data):
    """Encode binary data to base64."""
    return base64.b64encode(data).decode()

def decode_base64(data):
    """Decode base64 encoded data."""
    return base64.b64decode(data)

def hash_text_sha256(text):
    """Hash text with SHA-256."""
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()

def logger_debug(message):
    """Placeholder function for logging debug messages."""
    print(message)  # Replace with actual logging

def assemble_project_path(relative_path):
    """Assemble an absolute project path."""
    # This function needs to be defined based on your project's directory structure
    return os.path.join(os.path.dirname(__file__), relative_path)

def encode_image_path(image_path):
    """Encode image from a file path to base64."""
    with open(image_path, "rb") as image_file:
        encoded_image = encode_base64(image_file.read())
    return encoded_image

def encode_image_binary(image_binary, image_path=None):
    """Encode image binary data to base64."""
    encoded_image = encode_base64(image_binary)
    if image_path is not None:
        logger_debug(f'|>. img_hash {hash_text_sha256(encoded_image)}, path {image_path} .<|')
    return encoded_image

def decode_image(base64_encoded_image):
    """Decode a base64 encoded image to binary."""
    return decode_base64(base64_encoded_image)

def encode_data_to_base64_path(data: Any) -> List[str]:
    """Encode various types of data to base64 with appropriate data URI prefixes."""
    encoded_images = []

    if isinstance(data, (str, Image.Image, np.ndarray, bytes)):
        data = [data]

    for item in data:
        if isinstance(item, str):
            if os.path.exists(assemble_project_path(item)):
                path = assemble_project_path(item)
                encoded_image = encode_image_path(path)
                image_type = path.split(".")[-1].lower()
                encoded_image = f"data:image/{image_type};base64,{encoded_image}"
                encoded_images.append(encoded_image)
            else:
                encoded_images.append(item)
        elif isinstance(item, bytes):
            image = Image.frombytes('RGB', (1920, 1080), item, 'raw', 'BGRX')  # Size needs to be specified
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
        elif isinstance(item, Image.Image):
            buffered = io.BytesIO()
            item.save(buffered, format="JPEG")
        elif isinstance(item, np.ndarray):
            item = cv2.cvtColor(item, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(item)
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")

        encoded_image = encode_image_binary(buffered.getvalue())
        encoded_image = f"data:image/jpeg;base64,{encoded_image}"
        encoded_images.append(encoded_image)

    return encoded_images

def encode_single_data_to_base64(data: Any) -> str:
    # Process the single item
    if isinstance(data, str):
        # Check if the string is a file path
        if os.path.exists(assemble_project_path(data)):
            path = assemble_project_path(data)
            encoded_image = encode_image_path(path)
            image_type = path.split(".")[-1].lower()
            return f"data:image/{image_type};base64,{encoded_image}"
        else:
            # The string is not a file path, return as is
            return data
    elif isinstance(data, bytes):
        image = Image.frombytes('RGB', (1920, 1080), data, 'raw', 'BGRX')
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return f"data:image/jpeg;base64,{encode_image_binary(buffered.getvalue())}"
    elif isinstance(data, Image.Image):
        buffered = io.BytesIO()
        data.save(buffered, format="JPEG")
        return f"data:image/jpeg;base64,{encode_image_binary(buffered.getvalue())}"
    elif isinstance(data, np.ndarray):
        data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(data)
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return f"data:image/jpeg;base64,{encode_image_binary(buffered.getvalue())}"

    return ""
