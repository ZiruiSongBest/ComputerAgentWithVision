import os
import argparse
from utils.logger import Logger
import json
from datasets import load_dataset
from friday.agent.friday_agent import FridayAgent
from friday.core.executor import FridayExecutor
import dotenv

def main():
    parser = argparse.ArgumentParser(description='Inputs')
    parser.add_argument('--action_lib_path', type=str, default='friday/action_lib', help='tool repo path')
    parser.add_argument('--config_path', type=str, default='.env', help='openAI config file path')
    parser.add_argument('--query', type=str, default="use chrome to open youtube.com", help='Enter your task or simply press enter to execute the fallback task: "Move the text files containing the word \'agent\' from the folder named \'document\' to the path \'working_dir/agent\'"')
    parser.add_argument('--query_file_path', type=str, default='', help='Enter the path of the files for your task or leave empty if not applicable')
    parser.add_argument('--logging_filedir', type=str, default='log', help='log path')
    parser.add_argument('--logging_filename', type=str, default='temp.log', help='log file name')
    parser.add_argument('--logging_prefix', type=str, default=Logger.random_string(16), help='log file prefix')
    parser.add_argument('--score', type=int, default=4, help='critic score > score => store the tool')
    args = parser.parse_args()

    if not os.path.exists(args.logging_filedir):
        os.mkdir(args.logging_filedir)

    logging = Logger(log_dir=args.logging_filedir, log_filename=args.logging_filename, log_prefix=args.logging_prefix)

    friday_agent = FridayAgent(config_path=args.config_path, action_lib_dir=args.action_lib_path)
    planning_agent = friday_agent.planner
    retrieve_agent = friday_agent.retriever
    execute_agent = friday_agent.executor

    task = 'Your task is: {0}'.format(args.query)
    if args.query_file_path != '':
        task = task + '\nThe path of the files you need to use: {0}'.format(args.query_file_path)

    print('Task:\n'+task)
    logging.info(task)

    # relevant action
    retrieve_action_name = retrieve_agent.retrieve_action_name(task)
    retrieve_action_description_pair = retrieve_agent.retrieve_action_description_pair(retrieve_action_name)

    # task planner
    planning_agent.decompose_task(task, retrieve_action_description_pair)
    
    executor = FridayExecutor(planning_agent, execute_agent, retrieve_agent, logging, args.score)

    # iter each subtask
    while planning_agent.execute_list:
        type = planning_agent.execute_list[0]['type']
        if type == 'image':
            print('Image task')
            
        if executor.execute_task(task) == False:
            break

if __name__ == '__main__':
    dotenv.load_dotenv()
    main()

