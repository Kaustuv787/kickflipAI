#Author:Swastik Nayak
import os
import logging
import traceback

class Logger:
    def __init__(self,log_folder='logs',log_file='error.log'):
        self.log_folder=log_folder
        self.log_file=log_file
        self._ensure_log_folder_exists()
        self._setup_logger()

    def _ensure_log_folder_exists(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

    def _setup_logger(self):
        self.logger=logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        file_handler = logging.FileHandler(os.path.join(self.log_folder,self.log_file))
        formatter = logging.Formatter ('%(asctime)s -%(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_error(self, error):
        error_tags = traceback.format_exc()
        self.logger.error(f"{error}\n{error_tags}")
