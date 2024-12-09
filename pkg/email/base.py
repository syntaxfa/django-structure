from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EmailStruct:
    subject: str
    body: str
    receivers: List[str]
    sender: str
    link: Optional[str] = None


class Email(ABC):

    @abstractmethod
    def send_mail(self, subject: str, body: str, receivers: List[str], sender: str, link: Optional[str] = None):
        pass
