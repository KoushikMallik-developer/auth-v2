import abc
import logging
from abc import ABC


class BaseException(ABC, Exception):
    def __init__(self, msg):
        if msg:
            self.msg = msg
        else:
            self.msg = self.get_default_message
        logging.error(self.msg)

    @abc.abstractmethod
    def get_default_message(self):
        raise NotImplementedError()
