"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import logging
from queue import Queue
import threading

class LogProcessor:
    def __init__(self, queue: Queue = None, level=None, formatter = None, handlers=None):
        if queue is None or level is None or formatter is None or handlers is None:
            return
        self._queue = queue
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(level)
        self._logger.propagate = (
            False  # Do not propagate the message to be logged by the parents
        )
        for handler in handlers:
            handler.setLevel = level
            handler.setFormatter = formatter
            self._logger.addHandler(handler)

    def start(self):
        while True:
            try:
                record = self._queue.get()
                if record is not None:
                    self._logger.log(record.levelno, record.msg)
            except Exception as e:
                print(f'[LogProcessor::start] Exception - thread id: {threading.current_thread().ident}, logger: {self._logger}, queue: {self._queue}, e: {e}')
                pass