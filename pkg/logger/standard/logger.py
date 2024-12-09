import json
import logging
from typing import Dict, Optional

from pkg.logger.base import Log


class StandardLogger(Log):
    LOGGER_NAME = "syntax"

    def __init__(self):
        self.logger = self.get_logger()

    def get_logger(self) -> logging.Logger:
        # Create a logger
        logger = logging.getLogger(self.LOGGER_NAME)
        logger.setLevel(logging.DEBUG)

        # Create a formatter to define the log format
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s - %(app)s - %(category)s - %(sub_category)s - %(meta)s')

        # Create a file handler to write logs to a file
        # file_handler = logging.FileHandler('app.log')
        # file_handler.setLevel(logging.DEBUG)
        # file_handler.setFormatter(formatter)

        # Create a stream handler to print logs to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        # logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def debug(self, app: str,  msg: str, category: str, sub_category: str, meta: Optional[Dict] = None):
        self.logger.debug(
            msg=msg,
            extra={"app": app, "category": category, "sub_category": sub_category,
                   "meta": json.dumps(meta) if meta else {}})

    def info(self, app: str, msg: str, category: str, sub_category: str, meta: Optional[Dict] = None):
        self.logger.info(
            msg=msg,
            extra={"app": app, "category": category, "sub_category": sub_category,
                   "meta": json.dumps(meta) if meta else {}})

    def warn(self, app: str, msg: str, category: str, sub_category: str, meta: Optional[Dict] = None):
        self.logger.warning(
            msg=msg,
            extra={"app": app, "category": category, "sub_category": sub_category,
                   "meta": json.dumps(meta) if meta else {}})

    def error(self, app: str, msg: str, category: str, sub_category: str, meta: Optional[Dict] = None):
        self.logger.error(
            msg=msg,
            extra={"app": app, "category": category, "sub_category": sub_category,
                   "meta": json.dumps(meta) if meta else {}})
