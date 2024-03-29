import requests
import json
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8998")

# 测试加法
expression = "((46210 - 8*9068) / (2 - x))"
response = requests.post(
    BASE_URL + '/tools/calculator',
    json={'expression': expression}
)
print(response.json())