import json
import re
import os

from utils.logger import Logger
from utils import file_utils
from datetime import datetime


logger = Logger()
now = datetime.now()

def load_json(file_path):
    with open(file_path, mode='r', encoding='utf8') as fp:
        json_dict = json.load(fp)
        return json_dict

def json_append(json_data, new_key, new_value, prepend=True):
    new_dict = {new_key: new_value}
    if isinstance(json_data, list):
        # If we want to prepend and the list contains dictionaries or is empty
        if prepend or not json_data:
            json_data.insert(0, new_dict)
        # If we don't want to prepend, we append to the list
        else:
            json_data.append(new_dict)
    # If the data is not a list, we need to create a list to hold the new and existing data
    else:
        json_data = [new_dict, json_data] if prepend else [json_data, new_dict]

    return json_data


def save_json(json_dict, file_name, file_path=os.path.join(file_utils.get_project_root(), 'working_dir/log_json/'), indent=-1, date=True):
    if date:
        file_name = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{file_name}"
    file_path = os.path.join(file_path, file_name)
    
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    with open(file_path, mode='w', encoding='utf8') as fp:
        if indent == -1:
            json.dump(json_dict, fp, ensure_ascii=False)
        else:
            json.dump(json_dict, fp, ensure_ascii=False, indent=indent)


def check_json(json_string):
    try:
        json.loads(json_string)
    except:
        return False
    return True


def refine_json(json_string):
    patterns = [
        r"^`+json(.*?)`+", # ```json content```, ```json content``, ...
        r"^json(.*?)", # json content
        r"^json(.*?)\." # json content.
    ]

    for pattern in patterns:
        match = re.search(pattern, json_string, re.DOTALL)
        if match:
            json_string = match.group(1)
            if check_json(json_string):
                return json_string
    return json_string


def parse_semi_formatted_json(json_string):

    obj = None

    try:
        response = refine_json(json_string)
        obj = json.loads(response)

    except Exception as e:
        logger.error(f"Error in processing json: {e}. Object was: {json_string}.")
        logger.error_ex(e)

    return obj