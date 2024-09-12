from friday.core.tool_request_util import ToolRequestUtil

tool_request_util = ToolRequestUtil()

# Define the API path
api_path = "/tools/audio2text"

# Define the method to use
method = "post"

# Define the file path
file_path = '/home/ubuntu/workspace/GAIA/2023/test/5b89b147-cdab-40e1-be5b-819bc076c270.mp3'

# Since the API requires 'multipart/form-data', we need to pass the file in 'files' parameter
files = {'file': open(file_path, 'rb')}

# Specify the content type as required by the API
content_type = "multipart/form-data"

# Make the API request and get the response
response = tool_request_util.request(api_path=api_path, method=method, files=files, content_type=content_type)

# Print the response from the API
print(response)