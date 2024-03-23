import logging
import os
import sys
from colorama import Fore, Back, Style

class ColorFormatter(logging.Formatter):
    COLORS = {
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "DEBUG": Fore.GREEN,
        "INFO": Fore.WHITE,
        "CRITICAL": Fore.RED + Back.WHITE
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        record.msg = f"{color}{str(record.msg)}{Style.RESET_ALL}"
        if color:
            record.msg = color + record.msg + Style.RESET_ALL
        return super().format(record)

class Logger:
    def __init__(self, log_dir='log', log_filename='default.log', log_prefix=None, level=logging.INFO):
        self.log_dir = log_dir
        self.log_filename = log_filename
        self.log_prefix = log_prefix if log_prefix else self.random_string(16)
        self.level = level
        self.setup_logger()

    @staticmethod
    def random_string(length):
        import string
        import random
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def setup_logger(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        log_path = os.path.join(self.log_dir, self.log_filename)

        logger = logging.getLogger(self.log_prefix)
        logger.setLevel(self.level)

        formatter = logging.Formatter(f'[{self.log_prefix}] %(asctime)s - %(levelname)s - %(message)s')
        c_formatter = ColorFormatter(formatter._fmt)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(c_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        self.logger = logger

    def log(self, message, level=logging.INFO, title="", title_color=Fore.WHITE):
        if title:
            message = f"{title_color}{title}: {message}{Style.RESET_ALL}"
        self.logger.log(level, message)

    def critical(self, message, title=""): self.log(message, logging.CRITICAL, title)
    def error(self, message, title=""): self.log(message, logging.ERROR, title)
    def warn(self, message, title=""): self.log(message, logging.WARNING, title, Fore.YELLOW)
    def info(self, message, title=""): self.log(message, logging.INFO, title)
    def debug(self, message, title=""): self.log(message, logging.DEBUG, title, Fore.GREEN)