from friday.core.tool_request_util import ToolRequestUtil

tool_request_util = ToolRequestUtil()

# Define the API path
api_path = "/tools/bing/searchv2"

# Define the method to use
method = "get"

# Define the parameters for the API call
params = {
    "query": "August Wikipedia",
    "top_k": 1  # We want the top result only
}

# Define the content type
content_type = "application/json"

# Make the API call
response = tool_request_util.request(api_path, method, params=params, content_type=content_type)

# Print the response from the API
print(response)