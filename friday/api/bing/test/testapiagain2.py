from friday.core.tool_request_util import ToolRequestUtil

# Initialize the ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path and method
api_path = "/tools/bing/load_pagev2"
method = "get"

# Define the parameters for the API call
# Assuming we want to extract information from the Wikipedia page of Nobel Prizes
params = {
    "url": "https://en.wikipedia.org/wiki/List_of_Nobel_laureates",
    "query": None  # No specific query parameter is needed for this task
}

# Make the API call
response = tool_request_util.request(api_path=api_path, method=method, params=params, content_type="application/json")

# Print the return value of the API call
print(response)