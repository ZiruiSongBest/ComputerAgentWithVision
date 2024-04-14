import json

# File paths
original_file_path = 'Friday_GAIA_results/test.jsonl'
improved_file_path = 'Friday_GAIA_results/improved.jsonl'
metadata_file_path = 'test_metadata.jsonl'
output_file_path = 'output.jsonl'

# Read and collect task_ids with empty model_answer from test.jsonl
task_ids_with_empty_answers = []
with open(original_file_path, 'r') as file:
    for line in file:
        entry = json.loads(line)
        if entry.get('model_answer') == "":
            task_ids_with_empty_answers.append(entry['task_id'])

with open(improved_file_path, 'r') as file:
    for line in file:
        entry = json.loads(line)
        task_ids_with_empty_answers.remove(entry['task_id'])

# Map metadata to task_id
metadata_mapping = {}
with open(metadata_file_path, 'r') as file:
    for line in file:
        entry = json.loads(line)
        metadata_mapping[entry['task_id']] = entry

# Write new jsonl file with the required data
with open(output_file_path, 'w') as output_file:
    for task_id in task_ids_with_empty_answers:
        if task_id in metadata_mapping:
            meta = metadata_mapping[task_id]
            output_data = {
                "task_id": task_id,
                "Level": meta['Level'],
                "Question": meta['Question'],
                "file_name": meta['file_name']
            }
            json.dump(output_data, output_file)
            output_file.write('\n')

print(f"Data has been written to {output_file_path}.")
