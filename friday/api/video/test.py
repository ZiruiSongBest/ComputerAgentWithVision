import requests

url = 'http://localhost:8998/tools/video_qa'
data = {
    'prompt': 'Describe this video.',
    'video_url': '/Users/dylan/Downloads/BigBuckBunny_320x180.mp4',
    'start_time': 45,
    'end_time': 50
}

response = requests.post(url, data=data)
print(response.text)
