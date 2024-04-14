from datasets import load_dataset
import subprocess
import os
import json

# data_path = "/home/ubuntu/workspace/GAIA"
# dataset = load_dataset(data_path, "2023_level1")

question_set = "output.jsonl"
with open(question_set, 'r') as file:
    valid_data = [json.loads(line) for line in file]

# test_data = dataset["test"]
# valid_data = dataset["validation"]

conda_python_path = os.path.join(os.environ['CONDA_PREFIX'], 'python.exe')
working_directory = '..'

data_path = "/Users/dylan/Desktop/1Res/osc/ComputerAgentWithVisionDev/GAIA/2023/test"

for item in valid_data:
    task_id = item["task_id"]
    question = item["Question"]
    level = item["Level"]
    file_name = item["file_name"]
    file_path = ''
    if file_name != '':
        file_path = os.path.join(data_path, file_name)
    
    command = [
        'python', 'run.py', 
        '--query', question, 
        '--logging_filedir', f'log/{task_id}', 
        '--logging_filename', f'{task_id}.log', 
        '--logging_prefix', task_id
    ]
    
    if file_path != '':
        command.extend(['--query_file_path', file_path])
    
    with subprocess.Popen(command, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # 实时读取标准错误
        stderr_output = process.stderr.read()
        if stderr_output:
            print("STDERR:", stderr_output.strip())
    
    print('----------------------------------------')
    print('----------------------------------------')
