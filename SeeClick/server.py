import os
import torch
import socket
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import cv2
import datetime

app = Flask(__name__)

qwen_vl_chat_tokenizer = "/workspace/workspace/huggingface/hub/models--Qwen--Qwen-VL-Chat/"
seeclick_ckpt_dir = "/workspace/workspace/huggingface/hub/models--cckevinn--SeeClick/snapshots/b79618049920e209d15cda4d35004e32e8b485d9"

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(seeclick_ckpt_dir, device_map="cuda", trust_remote_code=True, bf16=True).eval()
model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)
prompt = "In this UI screenshot, what is the position of the element corresponding to the command \"{}\" (with point)?"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'Missing image or text data'}), 400
    
    file = request.files['image']
    text_data = request.form['text']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the image
    image_path = os.path.join('assets', file.filename)
    file.save(image_path)
    
    query = tokenizer.from_list_format([
        {'image': image_path},
        {'text': prompt.format(prompt, text_data)},
    ])
    
    response, history = model.chat(tokenizer, query=query, history=None)
    return jsonify({'dot_location': response})

if __name__ == '__main__':
    app.run(debug=True, host=socket.gethostname(), port=8998)
