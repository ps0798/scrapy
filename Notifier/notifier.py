from abc import ABC, abstractmethod
from enum import Enum

class NotifierType(Enum):

    CONSOLE = "console"
    TEXT_MESSAGE = "text_message"
    EMAIL = "email"

class Notifier(ABC):

    @abstractmethod
    def notify(self, msg):
        pass