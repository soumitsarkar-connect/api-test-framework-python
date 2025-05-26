import logging
import os

class Logger:
    _log_initialized = False  # Class-level flag

    def __init__(self, name="api-test", level=logging.DEBUG, log_file="logs/test.log"):
        self.logger = logging.getLogger(name)

        if not self.logger.handlers:
            self.logger.setLevel(level)
            os.makedirs(os.path.dirname(log_file), exist_ok=True)

            # Only clear the file once per run
            mode = 'w' if not Logger._log_initialized else 'a'
            Logger._log_initialized = True

            file_handler = logging.FileHandler(log_file, mode=mode)
            file_handler.setLevel(level)
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
