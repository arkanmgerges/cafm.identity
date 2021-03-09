"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import glob
import importlib
import json
import os
import signal
from time import sleep

from confluent_kafka.cimpl import KafkaError

import src.port_adapter.AppDi as AppDi
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.port_adapter.messaging.common.Consumer import Consumer
from src.port_adapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.port_adapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.port_adapter.messaging.common.model.IdentityEvent import IdentityEvent
from src.resource.logging.logger import logger


class ApiCommandListener:
    def __init__(self):
        self._handlers = []
        self._creatorServiceName = os.getenv('CAFM_IDENTITY_SERVICE_NAME', 'cafm.identity')
        self.addHandlers()
        self.targetsOnSuccess = []
        self.targetsOnException = []
        signal.signal(signal.SIGINT, self.interruptExecution)
        signal.signal(signal.SIGTERM, self.interruptExecution)

    def interruptExecution(self, _signum, _frame):
        raise SystemExit()

    def run(self):
        consumer: Consumer = AppDi.Builder.buildConsumer(
            groupId=os.getenv('CAFM_IDENTITY_CONSUMER_GROUP_API_CMD_NAME', ''), autoCommit=False, partitionEof=True,
            autoOffsetReset=ConsumerOffsetReset.earliest.name)

        # Subscribe
        consumer.subscribe([os.getenv('CAFM_API_COMMAND_TOPIC', '')])

        # Producer
        producer: TransactionalProducer = AppDi.instance.get(TransactionalProducer)
        producer.initTransaction()
        producer.beginTransaction()

        try:
            while True:
                try:
                    msg = consumer.poll(timeout=1.0)
                    if msg is None:
                        continue
                except Exception as _e:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.info(
                            f'[{ApiCommandListener.run.__qualname__}] msg reached partition eof: {msg.error()}')
                    else:
                        logger.error(msg.error())
                else:
                    isMsgProcessed = False
                    while not isMsgProcessed:
                        # Proper message
                        logger.info(
                            f'[{ApiCommandListener.run.__qualname__}] topic: {msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()} with key: {str(msg.key())}')
                        logger.info(f'value: {msg.value()}')

                        try:
                            msgData = msg.value()
                            logger.debug(f'[{ApiCommandListener.run.__qualname__}] received message data = {msgData}')
                            handledResult = self.handleCommand(messageData=msgData)
                            if handledResult is None:  # Consume the offset since there is no handler for it
                                logger.info(
                                    f'[{ApiCommandListener.run.__qualname__}] Consume the offset for handleCommand(name={msgData["name"]}, data={msgData["data"]}, metadata={msgData["metadata"]})')
                                producer.sendOffsetsToTransaction(consumer)
                                producer.commitTransaction()
                                producer.beginTransaction()
                                isMsgProcessed = True
                                continue

                            logger.debug(
                                f'[{ApiCommandListener.run.__qualname__}] handleResult returned with: {handledResult}')

                            if 'external' in msgData:
                                external = msgData['external']
                            else:
                                external = []

                            external.append({
                                'id': msgData['id'],
                                'creator_service_name': msgData['creator_service_name'],
                                'name': msgData['name'],
                                'version': msgData['version'],
                                'metadata': msgData['metadata'],
                                'data': msgData['data'],
                                'created_on': msgData['created_on']
                            })

                            for target in self.targetsOnSuccess:
                                logger.debug(f'ark1 -> {handledResult}')
                                res = target(messageData=msgData, creatorServiceName=self._creatorServiceName,
                                             resultData=handledResult['data'])
                                producer.produce(
                                    obj=res['obj'],
                                    schema=res['schema'])

                            # Produce the domain events
                            logger.debug(
                                f'[{ApiCommandListener.run.__qualname__}] get postponed events from the event publisher')
                            domainEvents = DomainPublishedEvents.postponedEvents()
                            for domainEvent in domainEvents:
                                logger.debug(
                                    f'[{ApiCommandListener.run.__qualname__}] produce domain event with name = {domainEvent.name()}')
                                producer.produce(
                                    obj=IdentityEvent(id=domainEvent.id(),
                                                      creatorServiceName=self._creatorServiceName,
                                                      name=domainEvent.name(),
                                                      metadata=msgData['metadata'],
                                                      data=json.dumps(domainEvent.data()),
                                                      createdOn=domainEvent.occurredOn(),
                                                      external=external),
                                    schema=IdentityEvent.get_schema())

                            logger.debug(f'[{ApiCommandListener.run.__qualname__}] cleanup event publisher')
                            DomainPublishedEvents.cleanup()
                            # Send the consumer's position to transaction to commit
                            # them along with the transaction, committing both
                            # input and outputs in the same transaction is what provides EOS.
                            producer.sendOffsetsToTransaction(consumer)
                            producer.commitTransaction()
                            producer.beginTransaction()
                            isMsgProcessed = True
                        except DomainModelException as e:
                            logger.warn(e)
                            msgData = msg.value()
                            for target in self.targetsOnException:
                                res = target(msgData, e, self._creatorServiceName)
                                producer.produce(
                                    obj=res['obj'],
                                    schema=res['schema'])
                            DomainPublishedEvents.cleanup()
                            producer.sendOffsetsToTransaction(consumer)
                            producer.commitTransaction()
                            producer.beginTransaction()
                            isMsgProcessed = True
                        except Exception as e:
                            DomainPublishedEvents.cleanup()
                            logger.error(e)
                            sleep(1)

                # sleep(3)
        except KeyboardInterrupt:
            logger.info(f'[{ApiCommandListener.run.__qualname__}] Aborted by user')
        except SystemExit:
            logger.info(f'[{ApiCommandListener.run.__qualname__}] Shutting down the process')
        finally:
            producer.abortTransaction()
            # Close down consumer to commit final offsets.
            consumer.close()

    def handleCommand(self, messageData: dict):
        for handler in self._handlers:
            name = messageData['name']
            metadata = messageData['metadata']

            if handler.canHandle(name):
                self.targetsOnSuccess = handler.targetsOnSuccess()
                self.targetsOnException = handler.targetsOnException()
                result = handler.handleCommand(messageData=messageData)
                return {"data": "", "metadata": metadata} if result is None else result
        return None

    def addHandlers(self):
        handlers = list(
            map(lambda x: x.strip('.py'),
                list(map(lambda x: x[x.find('src.port_adapter.messaging'):],
                         map(lambda x: x.replace('/', '.'),
                             filter(lambda x: x.find('__init__.py') == -1,
                                    glob.glob(f'{os.path.dirname(os.path.abspath(__file__))}/handler/**/*.py', recursive=True)))))))
        for handlerStr in handlers:
            m = importlib.import_module(handlerStr)
            handlerCls = getattr(m, handlerStr[handlerStr.rfind('.') + 1:])
            handler = handlerCls()
            self._handlers.append(handler)


ApiCommandListener().run()
