import base64
from Cradle.provider import OpenAIProvider

def analyze_image_with_prompts(image_path, prompts):
    # Initialize the LLM provider
    llm_provider_config_path = "./Vision/config/openai_config.json"
    llm_provider = OpenAIProvider()
    llm_provider.init_provider(llm_provider_config_path)

    # Define a function to encode the image to base64
    def encode_image(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Encode the provided image
    base64_image = encode_image(image_path)

    # Update the prompts with the base64 encoded image
    for prompt in prompts:
        for content in prompt["content"]:
            if content["type"] == "image_url":
                content["image_url"]["url"] = f"data:image/jpeg;base64,{base64_image}"

    # Send the message prompts to the LLM provider and get the response
    response, info = llm_provider.create_completion(prompts)

    return response, info

# Example usage of the function
image_path = "IMG_0389.JPG"
message_prompts = [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": ""  # This will be filled by the function
          }
        }
      ]
    }
]

response, info = analyze_image_with_prompts(image_path, message_prompts)
print(response)
print(info)
