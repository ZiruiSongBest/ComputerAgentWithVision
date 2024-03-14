import base64
from Cradle.provider import OpenAIProvider

llm_provider_config_path = "./Cradle/conf/openai_config.json"

llm_provider = OpenAIProvider()
llm_provider.init_provider(llm_provider_config_path)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image("IMG_0389.JPG")
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
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ]
response, info = llm_provider.create_completion(messages=message_prompts)
print(response)
print(info)