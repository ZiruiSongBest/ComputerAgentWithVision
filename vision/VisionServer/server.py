import os
# model_cache_directory = '/osc/model_cache'
# os.environ['HF_HOME'] = model_cache_directory
from transformers.file_utils import default_cache_path
cache_dir = default_cache_path
print(f"loading models from: {cache_dir}")

os.environ['CUDA_VISIBLE_DEVICES'] = '1'
import json
import socket
import base64
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import cv2

app = Flask(__name__)

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained('cckevinn/SeeClick', device_map="auto", trust_remote_code=True, bf16=True).eval()
model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

# Load second model
from OmniLMMChat import OmniLMMChat, img2base64
# chat_model = OmniLMMChat('openbmb/OmniLMM-12B') # or 'openbmb/MiniCPM-V'

@app.route('/seeclick', methods=['POST'])
def seeclick():
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'Missing image or text data'}), 400
    
    file = request.files['image']
    prompt = request.form['text']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the image
    image_path = os.path.join('assets', file.filename)
    file.save(image_path)
    
    query = tokenizer.from_list_format([
        {'image': image_path},
        {'text': prompt},
    ])
    
    response, history = model.chat(tokenizer, query=query, history=None)
    return jsonify({'dot_location': response})

@app.route('/omni', methods=['POST'])
def omnilmm():
    if 'image' not in request.form or 'content' not in request.form:
        return jsonify({'error': 'Missing image or content'}), 400

    content = request.form.get('content')
    base64_img = request.form.get('image')
    msgs = [{"role": "user", "content": content}]
    inputs = {"image": base64_img, "question": json.dumps(msgs)}

    response = chat_model.chat(inputs)
    
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True, host=socket.gethostname(), port=8998)