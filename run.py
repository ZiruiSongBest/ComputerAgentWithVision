import os
import argparse
from utils.logger import Logger
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
    parser.add_argument('--logging_prefix', type=str, default=Logger.random_string(4), help='log file prefix')
    parser.add_argument('--score', type=int, default=6, help='critic score > score => store the tool')
    args = parser.parse_args()

    friday_logging = Logger(log_dir=args.logging_filedir, log_filename=args.logging_filename, log_prefix=args.logging_prefix)
    friday_agent = FridayAgent(config_path=args.config_path, action_lib_dir=args.action_lib_path, logger=friday_logging)
    planning_agent = friday_agent.planner
    executor = FridayExecutor(planning_agent, friday_agent.executor, friday_agent.retriever, friday_logging, args.score)

    task = 'Your task is: {0}'.format(args.query)
    if args.query_file_path != '':
        task = task + '\nThe path of the files you need to use: {0}'.format(args.query_file_path)
    
    executor.plan_task(task)

    # iter each subtask
    while planning_agent.execute_list:
        type = planning_agent.action_node[planning_agent.execute_list[0]].type
        if type == 'Image':
            print('Image task')
            
        if executor.execute_task(task) == False:
            break

if __name__ == '__main__':
    dotenv.load_dotenv()
    main()