from friday.core.tool_request_util import ToolRequestUtil

tool_request_util = ToolRequestUtil()

# Define the parameters for the API call
params = {
    "prompt": "what character is playing the violin throughout the video?",
    "video_url": "https://www.youtube.com/watch?v=X-AjhXhk19U",
    "start_time": 45,
    "end_time": 50
}

# Make the API call
response = tool_request_util.request(
    api_path="/tools/video_qa",
    method="post",
    params=params,
    content_type="multipart/form-data"
)

# Print the return value of the API
print(response)