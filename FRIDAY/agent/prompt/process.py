import os

def read_content_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def extract_data_from_folder(folder_path):
    data_dict = {}
    # Iterate over all items in the given folder
    for item in sorted(os.listdir(folder_path)):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # Read the comment from the folder name
            comment = item.split('. ', 1)[-1]  # Split on the first dot and space, use the part after as the comment
            # Iterate over files in the numbered folder
            for file in os.listdir(item_path):
                file_path = os.path.join(item_path, file)
                # Assume the file name (without extension) is the key
                key = os.path.splitext(file)[0]
                # Read the content from the file
                content = read_content_from_file(file_path)
                # Use the comment as a comment for the key, and the content as the value
                data_dict[key] = (comment, content)
        else:
            # Files directly under the main folder (if any) can be processed similarly
            key = os.path.splitext(item)[0]
            content = read_content_from_file(item_path)
            data_dict[key] = ("", content)  # No comment for these entries
    return data_dict

def generate_python_file(output_file_path, data):
    with open(output_file_path, 'w') as py_file:
        py_file.write("prompt = {\n")
        for main_key, sub_dict in data.items():
            py_file.write(f"    '{main_key}' : {{\n")
            for sub_key, (comment, content) in sub_dict.items():
                if comment:  # Write the comment if it exists
                    py_file.write(f"        # {comment}\n")
                py_file.write(f"        '{sub_key}': '''\n{content}\n''',\n")
            py_file.write("    },\n")
        py_file.write("}\n")

# Main execution starts here
input_folder = './prompt'
output_python_file = '../prompt.py'

# Data structure to hold the entire content
prompt_data = {}

# Read the folder structure and extract data
for main_folder in os.listdir(input_folder):
    main_folder_path = os.path.join(input_folder, main_folder)
    if os.path.isdir(main_folder_path):
        prompt_data[main_folder] = extract_data_from_folder(main_folder_path)

# Generate the output Python file
generate_python_file(output_python_file, prompt_data)

print("Python file has been successfully generated.")
