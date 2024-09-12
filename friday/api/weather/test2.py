from friday.core.tool_request_util import ToolRequestUtil
tool_request_util = ToolRequestUtil()

# Define the API path and method
api_path = "/weather/query"
method = "get"

# Define the parameters for the API call
# Assuming today's date is required, we use a placeholder '2023-04-01' for demonstration.
# In a real scenario, you would dynamically generate today's date in the format 'YYYY-MM-DD'.
params = {
    "date": "2023-04-01",
    "city": "Beijing"
}

# Make the API call
response = tool_request_util.request(api_path, method, params=params)

# Print the return value of the API
print(response)