"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import glob
import importlib
import os
import signal
from abc import abstractmethod
from time import sleep
from typing import List

from confluent_kafka.cimpl import KafkaError

import src.port_adapter.AppDi as AppDi
from src.port_adapter.messaging.common.Consumer import Consumer
from src.port_adapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.port_adapter.messaging.common.TransactionalProducer import (
    TransactionalProducer,
)
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.resource.logging.logger import logger


class CommonListener:
    def __init__(self, creatorServiceName, handlersPath):
        self._handlers = []
        self._creatorServiceName = os.getenv(
            "CAFM_PROJECT_SERVICE_NAME", "cafm.identity"
        )
        self._cafmApiServiceName = os.getenv("CAFM_API_SERVICE_NAME", "cafm.api")
        self._addHandlers(handlersPath)
        self.targetsOnSuccess = []
        self.targetsOnException = []
        signal.signal(signal.SIGINT, self.interruptExecution)
        signal.signal(signal.SIGTERM, self.interruptExecution)

    def interruptExecution(self, _signum, _frame):
        raise SystemExit()

    def _addHandlers(self, handlersPath):
        handlers = list(
            map(
                lambda x: x.strip(".py"),
                list(
                    map(
                        lambda x: x[x.find("src.port_adapter.messaging") :],
                        map(
                            lambda x: x.replace("/", "."),
                            filter(
                                lambda x: x.find("__init__.py") == -1,
                                glob.glob(
                                    handlersPath,
                                    recursive=True,
                                ),
                            ),
                        ),
                    )
                ),
            )
        )
        for handlerStr in handlers:
            m = importlib.import_module(handlerStr)
            handlerCls = getattr(m, handlerStr[handlerStr.rfind(".") + 1 :])
            handler = handlerCls()
            self._handlers.append(handler)

    def _process(self, consumerGroupId, consumerTopicList: List[str]):
        consumer: Consumer = AppDi.Builder.buildConsumer(
            groupId=consumerGroupId,
            autoCommit=False,
            partitionEof=True,
            autoOffsetReset=ConsumerOffsetReset.earliest.name,
        )

        # Subscribe - Consume the commands that exist in this service own topic
        consumer.subscribe(consumerTopicList)

        # Producer
        producer: TransactionalProducer = AppDi.instance.get(TransactionalProducer)
        producer.initTransaction()
        producer.beginTransaction()

        try:
            while True:
                try:
                    message = consumer.poll(timeout=1.0)
                    if message is None:
                        continue
                except Exception as _e:
                    continue

                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        logger.info(
                            f"[{CommonListener._process.__qualname__}] message reached partition eof: {message.error()}"
                        )
                    else:
                        logger.error(message.error())
                else:
                    # Proper message
                    logger.info(
                        f"[{CommonListener._process.__qualname__}] topic: {message.topic()}, partition: {message.partition()}, offset: {message.offset()} with key: {str(message.key())}"
                    )
                    logger.info(f"value: {message.value()}")

                    messageData = message.value()
                    logger.debug(
                        f"[{CommonListener._process.__qualname__}] received message data = {messageData}"
                    )

                    for handler in self._handlers:
                        name = messageData["name"]
                        metadata = messageData["metadata"]

                        if handler.canHandle(name):
                            isMessageProcessed = False
                            while not isMessageProcessed:
                                try:
                                    handledResult = self._handleCommand(
                                        handler=handler, messageData=messageData
                                    )
                                    self._processHandledResult(
                                        producer=producer,
                                        consumer=consumer,
                                        handledResult=handledResult,
                                        messageData=messageData,
                                    )
                                    isMessageProcessed = True
                                except Exception as e:
                                    sleep(1)
                    producer.sendOffsetsToTransaction(consumer)
                    producer.commitTransaction()
                    producer.beginTransaction()
        except KeyboardInterrupt:
            logger.info(f"[{CommonListener._process.__qualname__}] Aborted by user")
        except SystemExit:
            logger.info(
                f"[{CommonListener._process.__qualname__}] Shutting down the process"
            )
        finally:
            producer.abortTransaction()
            # Close down consumer to commit final offsets.
            consumer.close()

    @abstractmethod
    def _processHandledResult(self, producer, consumer, handledResult, messageData):
        pass

    def _handleCommand(self, handler, messageData: dict):
        name = messageData["name"]
        metadata = messageData["metadata"]
        if name == CommonCommandConstant.PROCESS_BULK.value:
            result = handler.handleCommand(
                messageData=messageData, extraData={"handlers": self._handlers}
            )
        else:
            result = handler.handleCommand(messageData=messageData)
        return {"data": "", "metadata": metadata} if result is None else result
