import requests
import json
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8998")

response = requests.get(
    BASE_URL + '/tools/arxiv',
    json={'query': 'BenchLMM'}
)

# print(response.json())
print(json.dumps(response.json(), indent=4))