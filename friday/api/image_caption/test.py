import requests

url = "http://localhost:8998/tools/image_caption"

files = {'image_file': ('birds.jpg', open('birds.jpg', 'rb'), 'image/jpeg')}

# 这里是表单数据，你可以根据需要修改
data = {
    'query': "What's in this image?"
    # 如果你还想通过URL发送图像，你可以这样做
    # 'url': 'http://example.com/path/to/image.jpg'
}

# 发送请求
response = requests.post(url, files=files, data=data)

# 输出响应数据
print(response.json())
