import os
import ast

# Read the content of your Python file

input_file_path = '../prompt.py'
output_folder = '../prompt'

with open(input_file_path, 'r') as file:
    input_content = file.read()

# Parse the content as a Python AST (Abstract Syntax Tree)
parsed_content = ast.parse(input_content)

# Function to extract the dictionary from the AST
def extract_dict(node):
    if isinstance(node, ast.Dict):
        return {ast.literal_eval(k): ast.literal_eval(v) for k, v in zip(node.keys, node.values)}
    for child_node in ast.iter_child_nodes(node):
        result = extract_dict(child_node)
        if result is not None:
            return result

# Extract the main dictionary from the parsed content
main_dict = extract_dict(parsed_content)

# Function to write content to files
def write_content_to_file(folder_path, file_name, content):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{file_name}.txt")
    with open(file_path, 'w') as file:
        # Strip leading whitespace from each line
        content = '\n'.join(line.lstrip() for line in content.strip().split('\n'))
        file.write(content)

# Iterate over the main dictionary and create folders and files
for main_key, sub_dict in main_dict.items():
    for sub_key, content in sub_dict.items():
        # Define folder and file names
        folder_path = os.path.join(output_folder, main_key)
        file_name = sub_key

        # Write the content to the file
        write_content_to_file(folder_path, file_name, content)

print("Content has been successfully extracted and saved in the folder structure.")
