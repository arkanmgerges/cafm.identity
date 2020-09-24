import inspect
import logging
import os
import sys
import traceback
from logging import Logger
from types import TracebackType
from typing import Text, Union, Any, Optional, Dict, Tuple
from injector import Module, singleton, provider, Injector

from src.resource.logging.CustomLogger import CustomLogger


class Di(Module):
    """
    Dependency injection module of the app

    """
    @singleton
    @provider
    def provideLogger(self) -> Logger:
        loggerLevel = 'DEBUG'
        try:
            loggerLevel = str.upper(os.environ['CORAL_API_LOGGING'])
            hasLoggerLevel = getattr(logging, loggerLevel, 'None') > 0
            if hasLoggerLevel:
                if loggerLevel not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                    loggerLevel = 'NOTSET'
        except:
            loggerLevel = 'NOTSET'

        logger = CustomLogger('coralLogger')
        # logger = logging.getLogger('coralLogger')
        logger.setLevel(loggerLevel)
        if loggerLevel != 'NOTSET':
            ch = logging.StreamHandler()
            ch.setLevel(loggerLevel)
            formatter = logging.Formatter('%(asctime)s - [coral.api] - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            logger.propagate = False  # Do not propagate the message to be logged by the parents
            logger.addHandler(ch)
        else:
            logger.disabled = True
        return logger


instance = Injector([Di])
