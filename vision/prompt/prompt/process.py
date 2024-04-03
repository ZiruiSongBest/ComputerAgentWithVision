import os

def read_txt_files_and_generate_py(directory, output_file):
    prompts = {}
    
    # Read all .txt files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(filename, 'r') as file:
                # Remove the '.txt' extension and use the filename as the key
                key = filename[:-4]
                # Read the content and strip any leading/trailing whitespace
                content = file.read().strip()
                prompts[key] = content
    
    # Write the prompts dictionary to the output Python file
    with open(output_file, 'w') as py_file:
        py_file.write("prompt = {\n")
        for key, content in prompts.items():
            py_file.write(f"    '{key}': '''\n{content}\n''',\n")
        py_file.write("}\n")

# Set the current directory and output file name
current_directory = '.'
output_python_file = '../prompt.py'

# Call the function with the current directory and desired output file
read_txt_files_and_generate_py(current_directory, output_python_file)

print("prompt.py file has been successfully generated.")
