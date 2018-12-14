import logging
import re
from logging.handlers import TimedRotatingFileHandler


class Logger(object):
    # 自定义logging
    def __init__(self):
        self.logger = logging.getLogger('FlaskAll')
        self.logger.setLevel(logging.INFO)
        log_format = "[%(asctime)s] %(levelname)s %(name)s %(filename)s : %(message)s"
        formater = logging.Formatter(log_format)
        log_file_handler = TimedRotatingFileHandler(filename="./log/flask.log", when="M", interval=2, backupCount=3)
        log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
        log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
        log_file_handler.setFormatter(formater)
        self.logger.addHandler(log_file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)
