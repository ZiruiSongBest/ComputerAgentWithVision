from datasets import load_dataset
import subprocess
import os
from excel_util import ExcelWriter, read_file_content

data_path = "/home/ubuntu/workspace/GAIA"
dataset = load_dataset(data_path, "2023_level1")

test_data = dataset["test"]
valid_data = dataset["validation"]

conda_python_path = os.path.join(os.environ['CONDA_PREFIX'], 'python.exe')
# conda_python_path = '/Users/dylan/miniconda3/envs/test/bin/python'
# conda_python_path = '/home/ubuntu/anaconda3/envs/osc/bin/python'
working_directory = '..'

writer = ExcelWriter('tasks.xlsx')

for item in test_data:
    task_id = item["task_id"]
    question = item["Question"]
    level = item["Level"]
    final_answer = item["Final answer"]
    file_name = item["file_name"]
    file_path = item["file_path"]
    annotator_metadata = item["Annotator Metadata"]
    
    if file_path == '':
        continue
    
    command = [
        'python', 'run.py', 
        '--query', question, 
        '--logging_filedir', f'log/{task_id}', 
        '--logging_filename', f'{task_id}.log', 
        '--logging_prefix', task_id
    ]
    
    if file_path != '':
        command.extend(['--query_file_path', file_path])
    
    result = subprocess.run(command, cwd=working_directory, capture_output=True, text=True)
    
    
    final_result = read_file_content(os.path.join(working_directory, f'log/{task_id}/final_result.txt'))
    writer.add_row(task_id, final_answer)
    
    # print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)