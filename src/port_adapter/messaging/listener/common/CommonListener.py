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
from src.port_adapter.messaging.listener.common.ProcessHandleData import ProcessHandleData
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
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
                    logger.debug(f"[{CommonListener._process.__qualname__}] received message data = {messageData}")

                    processHandleDataList: List[ProcessHandleData] = []
                    for handler in self._handlers:
                        name = messageData["name"]
                        metadata = messageData["metadata"]

                        if handler.canHandle(name):
                            isMessageProcessed = False
                            while not isMessageProcessed:
                                try:
                                    handledResult = self._handleCommand(handler=handler, messageData=messageData)
                                    processHandleData = ProcessHandleData(
                                        producer=producer,
                                        consumer=consumer,
                                        handledResult=handledResult,
                                        messageData=messageData,
                                        handler=handler,
                                    )
                                    self._processHandledResult(processHandleData=processHandleData)
                                    processHandleDataList.append(processHandleData)
                                    isMessageProcessed = True
                                except Exception as e:
                                    logger.error(e)
                                    sleep(1)
                    for processHandleDataItem in processHandleDataList:
                        if processHandleDataItem.isSuccess:
                            self._handleTargetsOnSuccess(processHandleData=processHandleDataItem)
                        elif not processHandleDataItem.isSuccess:
                            self._handleTargetsOnException(processHandleData=processHandleDataItem)

                    producer.sendOffsetsToTransaction(consumer)
                    producer.commitTransaction()
                    producer.beginTransaction()
        except KeyboardInterrupt:
            logger.info(f"[{CommonListener._process.__qualname__}] Aborted by user")
        except SystemExit:
            logger.info(f"[{CommonListener._process.__qualname__}] Shutting down the process")
        finally:
            producer.abortTransaction()
            # Close down consumer to commit final offsets.
            consumer.close()

    def _handleTargetsOnSuccess(self, processHandleData: ProcessHandleData):
        handler: Handler = processHandleData.handler
        messageData = processHandleData.messageData
        handledResult = processHandleData.handledResult
        producer = processHandleData.producer
        for target in handler.targetsOnSuccess():
            res = target(
                messageData=messageData,
                creatorServiceName=self._creatorServiceName,
                resultData=handledResult["data"],
            )
            producer.produce(obj=res["obj"], schema=res["schema"])

    def _handleTargetsOnException(self, processHandleData: ProcessHandleData):
        handler = processHandleData.handler
        messageData = processHandleData.messageData
        e = processHandleData.exception
        producer = processHandleData.producer
        for target in handler.targetsOnException():
            res = target(messageData, e, self._creatorServiceName)
            producer.produce(obj=res["obj"], schema=res["schema"])

    @abstractmethod
    def _processHandledResult(self, processHandleData: ProcessHandleData):
        pass

    def _handleCommand(self, handler, messageData: dict):
        name = messageData["name"]
        metadata = messageData["metadata"]
        if name == CommonCommandConstant.PROCESS_BULK.value:
            result = handler.handleCommand(messageData=messageData, extraData={"handlers": self._handlers})
        else:
            result = handler.handleCommand(messageData=messageData)
        return {"data": "", "metadata": metadata} if result is None else result
