from typing import Dict, Optional
from abc import ABC, abstractmethod


class Log(ABC):

    @abstractmethod
    def debug(self, app: str, msg: str, category: str, sub_category: str, meta: Optional[Dict] = dict):
        pass

    @abstractmethod
    def info(self, app: str, msg: str, category: str, sub_category: str, meta: Optional[Dict] = dict):
        pass

    @abstractmethod
    def warn(self, app: str, msg: str, category: str, sub_category: str, meta: Optional[Dict] = dict):
        pass

    @abstractmethod
    def error(self, app: str, msg: str, category: str, sub_category: str, meta: Optional[Dict] = dict):
        pass
