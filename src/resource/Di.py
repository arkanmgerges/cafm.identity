import logging
import os
from logging import Logger
from logging.handlers import QueueHandler
from queue import Queue

from injector import Module, singleton, provider, Injector

from src.resource.logging.LogProcessor import LogProcessor


class Di(Module):
    """
    Dependency injection module of the app

    """

    @singleton
    @provider
    def provideLoggerQueue(self) -> Queue:
        return Queue(-1)

    @singleton
    @provider
    def provideLogProcessor(self) -> LogProcessor:
        from src.resource.logging.CustomLogger import LogLevelEnum
        loggerLevel = LogLevelEnum.DEBUG
        try:
            loggerLevel = os.getenv("CAFM_IDENTITY_LOGGING", LogLevelEnum.NOTSET)
            if loggerLevel != LogLevelEnum.NOTSET:
                if loggerLevel not in [logLevel.name for logLevel in LogLevelEnum]:
                    loggerLevel = LogLevelEnum.NOTSET
                else:
                    from src.resource.logging.CustomLogger import logLevelEnumItemFromString
                    loggerLevel = logLevelEnumItemFromString(loggerLevel)
        except:
            loggerLevel = LogLevelEnum.NOTSET
        queue = self.__injector__.get(Queue)

        if loggerLevel != LogLevelEnum.NOTSET:
            from src.resource.logging.CustomLoggerFormatter import CustomLoggerFormatter
            return LogProcessor(queue=queue, formatter=CustomLoggerFormatter(), level=loggerLevel.name, handlers=[logging.StreamHandler()])
        return LogProcessor()

    @provider
    def provideLogger(self) -> Logger:
        from src.resource.logging.CustomLogger import LogLevelEnum
        loggerLevel = LogLevelEnum.DEBUG
        try:
            loggerLevel = os.getenv("CAFM_IDENTITY_LOGGING", LogLevelEnum.NOTSET)
            if loggerLevel != LogLevelEnum.NOTSET:
                if loggerLevel not in [logLevel.name for logLevel in LogLevelEnum]:
                    loggerLevel = LogLevelEnum.NOTSET
                else:
                    from src.resource.logging.CustomLogger import logLevelEnumItemFromString
                    loggerLevel = logLevelEnumItemFromString(loggerLevel)
        except:
            loggerLevel = LogLevelEnum.NOTSET

        from src.resource.logging.CustomLogger import CustomLogger
        logger = CustomLogger("cafmLogger")
        if loggerLevel != LogLevelEnum.NOTSET:
            queue = self.__injector__.get(Queue)
            handler = QueueHandler(queue)
            logger.addHandler(handler)
        else:
            logger.disabled = True
        return logger


instance = Injector([Di])
