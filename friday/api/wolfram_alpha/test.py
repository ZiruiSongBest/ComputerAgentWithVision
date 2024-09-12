import requests
import json
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8998")

# API endpoint
url = f"{BASE_URL}/tools/wolframalpha"

# Headers
headers = {
    'Content-Type': 'application/json'
}

# Data
data = {
    "query": "5+6"
}

# Send the request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Print the response
print(response.json())