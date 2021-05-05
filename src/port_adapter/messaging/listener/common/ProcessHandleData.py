"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.Handler import Handler


class ProcessHandleData:
    def __init__(self, producer, consumer, handledResult, messageData, handler):
        self.producer = producer
        self.consumer = consumer
        self.handledResult = handledResult
        self.messageData = messageData
        self.handler: Handler = handler
        self.isSuccess = None
        self.exception = None