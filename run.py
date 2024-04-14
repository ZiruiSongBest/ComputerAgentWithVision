import argparse
import os
from utils.logger import Logger
from friday.agent.friday_agent import FridayAgent
from friday.core.friday_executor import FridayExecutor
from vision.core.vision import Vision

import dotenv

def main():
    parser = argparse.ArgumentParser(description='Inputs')
    parser.add_argument('--action_lib_path', type=str, default='friday/action_lib', help='tool repo path')
    parser.add_argument('--config_path', type=str, default='.env', help='openAI config file path')
    parser.add_argument('--query', type=str, default="I want to open google chrome browser, and use vision actions to search Sound Euphonium", help='Enter your task or simply press enter to execute the fallback task: "Move the text files containing the word \'agent\' from the folder named \'document\' to the path \'working_dir/agent\'"')
    parser.add_argument('--query_file_path', type=str, default='', help='Enter the path of the files for your task or leave empty if not applicable')
    parser.add_argument('--logging_filedir', type=str, default='log', help='log path')
    parser.add_argument('--logging_filename', type=str, default='temp.log', help='log file name')
    parser.add_argument('--logging_prefix', type=str, default=Logger.random_string(4), help='log file prefix')
    parser.add_argument('--score', type=int, default=8, help='critic score > score => store the tool')
    args = parser.parse_args()

    if args.logging_filedir != 'log' and os.path.exists(args.logging_filedir):
        return

    logging_logger = Logger(log_dir=args.logging_filedir, log_filename=args.logging_filename, log_prefix=args.logging_prefix)
    friday_agent = FridayAgent(config_path=args.config_path, action_lib_dir=args.action_lib_path, logger=logging_logger)
    planning_agent = friday_agent.planner
    executor = FridayExecutor(planning_agent, friday_agent.executor, friday_agent.retriever, logging_logger, args.score)
    vision_executor = Vision(logger=logging_logger)

    task = 'Your task is: {0}'.format(args.query)
    if args.query_file_path != '':
        task = task + '\nThe path of the files you need to use: {0}'.format(args.query_file_path)
    
    executor.plan_task(task)
    planed = 1

    # iter each subtask
    while planning_agent.execute_list:
        overall_result = {}
        action = planning_agent.execute_list[0] # name, str
        action_node = planning_agent.action_node[action] # action_node: name, description, return_val, relevant_code, next_action, status, type, detail
        description = action_node.description
        pre_tasks_info = planning_agent.get_pre_tasks_info(action)
        type = planning_agent.action_node[planning_agent.execute_list[0]].type # '{"open_google_chrome": {"description": "Execute a system command to open Google Chrome on macOS.", "return_val": ["\\nNone\\n"]}}'
        logging_logger.info("The current subtask is: {subtask}".format(subtask=description), title=f'Current {type} Task', color='red')
        
        if type == 'Vision':
            actions = []
            action_nodes = []
            for execute_action in planning_agent.execute_list:
                if planning_agent.action_node[execute_action].type == 'Vision':
                    actions.append(execute_action)
                    action_nodes.append(planning_agent.action_node[execute_action])
                    planning_agent.execute_list.remove(execute_action)
                else:
                    break
            planning_agent.execute_list.insert(0, action)
            return_val = vision_executor.global_execute(task, actions, action_nodes, pre_tasks_info)
            planning_agent.execute_list.remove(action)
        else:
            return_val = executor.execute_task(task, action, action_node, pre_tasks_info)
        
        if return_val[0] == 'fail' and planed < 3:
            # planning_agent.redecompose_task(task, action)
            executor.plan_task(task, replan=True)
            planed += 1
        elif return_val[0] == 'replan':
            continue
        elif return_val[0] == 'success':
            _, result, relevant_code = return_val
            print("Current task execution completed!!!")
            
            if result != None and result != '':
                with open(os.path.join(args.logging_filedir, 'result.txt'), 'a') as f:
                    f.write(f'{action}: {result} \n')
                with open(os.path.join(args.logging_filedir, 'final_result.txt'), 'w') as f:
                    f.write(f'{action}: {result.strip()} \n')
            planning_agent.update_action(action, result, relevant_code, True, type)
            planning_agent.execute_list.remove(action)

if __name__ == '__main__':
    dotenv.load_dotenv()
    main()