import os
import argparse
from utils.logger import Logger


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

logger = Logger(log_dir=args.logging_filedir, log_filename=args.logging_filename, log_prefix=args.logging_prefix)

logger.info(message="test message", title="this is title", color="blue")