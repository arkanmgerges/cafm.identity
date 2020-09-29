import inspect
import logging
import os
import sys
import traceback
from logging import Logger
from types import TracebackType
from typing import Text, Union, Any, Optional, Dict, Tuple
from injector import Module, singleton, provider, Injector

from src.resource.logging.CustomLogger import CustomLogger, LogLevelEnum, logLevelEnumItemFromString
from src.resource.logging.CustomLoggerFormatter import CustomLoggerFormatter


class Di(Module):
    """
    Dependency injection module of the app

    """

    @singleton
    @provider
    def provideLogger(self) -> Logger:
        loggerLevel = LogLevelEnum.DEBUG
        try:
            loggerLevel = os.getenv('CORAL_IDENTITY_LOGGING', LogLevelEnum.NOTSET)
            if loggerLevel != LogLevelEnum.NOTSET:
                if loggerLevel not in [logLevel.name for logLevel in LogLevelEnum]:
                    loggerLevel = LogLevelEnum.NOTSET
                else:
                    loggerLevel = logLevelEnumItemFromString(loggerLevel)
        except:
            loggerLevel = LogLevelEnum.NOTSET

        logger = CustomLogger('coralLogger')
        if loggerLevel != LogLevelEnum.NOTSET:
            ch = logging.StreamHandler()
            ch.setLevel(loggerLevel.name)
            ch.setFormatter(CustomLoggerFormatter())
            logger.propagate = False  # Do not propagate the message to be logged by the parents
            logger.addHandler(ch)
        else:
            logger.disabled = True
        return logger


instance = Injector([Di])
