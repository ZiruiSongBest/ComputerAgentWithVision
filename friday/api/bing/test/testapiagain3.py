from friday.core.tool_request_util import ToolRequestUtil

tool_request_util = ToolRequestUtil()

# URL obtained from the 'search_wikipedia_page' context
url = "https://en.wikipedia.org/wiki/West_African_Vodun"

# Setting the 'query' parameter to target sections likely to contain in-text citations
# Since the API documentation does not specify how to target specific sections for in-text citations,
# we will not use the 'query' parameter for this purpose. Instead, we load the entire page.
params = {
    "url": url,
    "query": None  # Not targeting specific sections as the API does not support this directly
}

# Calling the specified API to load the content of the West African Vodun Wikipedia page
response = tool_request_util.request(api_path="/tools/bing/load_pagev2", method="get", params=params, content_type="application/json")

# Printing the return value of the API
print(response)