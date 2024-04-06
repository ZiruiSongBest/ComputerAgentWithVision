import openai
import json
import logging
import tiktoken
import os
from dotenv import load_dotenv


load_dotenv()
MODEL_NAME = os.getenv('MODEL_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')


class OpenAI:
    """
      OPEN AI Chat Models
    """
    def __init__(self, config_path=None):

        self.model_name = MODEL_NAME
        openai.api_key = OPENAI_API_KEY
        openai.organization = OPENAI_ORGANIZATION
        # print(openai.api_key)
        # print(openai.organization)
        # openai.proxy = proxy

    def chat(self, messages, temperature=0, sleep_time=2):
        if (self.num_tokens(messages) > 20000):
            raise ValueError("The number of tokens in the messages exceeds the limit of 10000 tokens.")
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature
        )
        logging.info(f"Response: {response.choices[0].message.content}")

        # time.sleep(sleep_time)
        # return response['choices'][0]['message']
        return response.choices[0].message.content
    
    def num_tokens(self, messages: list, encoding_name: str = 'gpt-4-turbo-preview') -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model(encoding_name)
        num_tokens = 0
        for msg in messages:
            num_tokens += len(encoding.encode(msg['content']))
        return num_tokens


