from friday.core.tool_request_util import ToolRequestUtil

tool_request_util = ToolRequestUtil()

# Define the API path
api_path = "/tools/video_qa"

# Specify the method to use for the request
method = "post"

# Define the parameters for the API request
params = {
    "start_time": 45,
    "end_time": 50
}

# Specify the file to be uploaded
files = {
    "video_file": ("/Users/dylan/Downloads/BigBuckBunny_320x180.mp4", open("/Users/dylan/Downloads/BigBuckBunny_320x180.mp4", "rb"))
}

# Specify the content type for the request
content_type = "multipart/form-data"

# Make the API request and print the return value
response = tool_request_util.request(api_path=api_path, method=method, params=params, files=files, content_type=content_type)
print(response)