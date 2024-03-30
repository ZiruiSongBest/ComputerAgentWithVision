import requests

# Define the base URL of the API
BASE_URL = "http://localhost:8998"  # Change this to the actual base URL

# Define the API endpoint for Bing Search V2
api_endpoint = "/tools/bing/searchv2"

# Parameters to be sent in the query string
params = {
    "query": "OpenAI",
    "top_k": 10  # Optional, specify the number of top results you want
}

# Send the GET request with parameters
response = requests.get(f"{BASE_URL}{api_endpoint}", params=params)

# Check if the response is successful
if response.status_code == 200:
    # Process the successful response
    print("Response:", response.json())
else:
    # Handle errors
    print(f"Error: Received status code {response.status_code}")
    print("Message:", response.text)
