import inspect
import logging
import os
import sys
import traceback
from logging import Logger
from types import TracebackType
from typing import Text, Union, Any, Optional, Dict, Tuple

_SysExcInfoType = Union[Tuple[type, BaseException, Optional[TracebackType]],
                        Tuple[None, None, None]]
from injector import Module, singleton, provider, Injector

if sys.version_info >= (3, 5):
    _ExcInfoType = Union[None, bool, _SysExcInfoType, BaseException]
else:
    _ExcInfoType = Union[None, bool, _SysExcInfoType]


class CustomLogger(Logger):
    def __init__(self, name: str, level: Union[int, Text] = 0):
        super().__init__(name, level)

    def debug(self, msg: Any, *args: Any, exc_info: _ExcInfoType = ...,
              stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
              **kwargs: Any) -> None:
        self.modifyMsg(super().debug, msg)

    def info(self, msg: Any, *args: Any, excInfo: _ExcInfoType = ...,
             stackInfo: bool = False, stackLevel: int = 0, extra: Optional[Dict[str, Any]] = None,
             **kwargs: Any) -> None:
        self.modifyMsg(super().info, msg)

    def warning(self, msg: Any, *args: Any, exc_info: _ExcInfoType = ...,
                stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
                **kwargs: Any) -> None:
        self.modifyMsg(super().warning, msg)

    def warn(self, msg: Any, *args: Any, exc_info: _ExcInfoType = ...,
             stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
             **kwargs: Any) -> None:
        self.modifyMsg(super().warn, msg)

    def error(self, msg: Any, *args: Any, exc_info: _ExcInfoType = ...,
              stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
              **kwargs: Any) -> None:
        self.modifyMsg(super().error, msg, True)

    def exception(self, msg: Any, *args: Any, exc_info: _ExcInfoType = ...,
                  stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
                  **kwargs: Any) -> None:
        self.modifyMsg(super().exception, msg, True)

    def critical(self, msg: Any, *args: Any, exc_info: _ExcInfoType = ...,
                 stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
                 **kwargs: Any) -> None:
        self.modifyMsg(super().critical, msg)

    def log(self, level: int, msg: Any, *args: Any, exc_info: _ExcInfoType = ...,
            stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
            **kwargs: Any) -> None:
        self.modifyMsg(super().log, msg)

    def modifyMsg(self, call, msg, printStackTrace=False):
        callerFrameRecord = inspect.stack()[1]
        frame = callerFrameRecord[0]
        info = inspect.getframeinfo(frame)
        modifiedMsg = f'[{info.filename}][line: {info.lineno}] {msg}'
        call(modifiedMsg)
        if printStackTrace:
            traceback.print_stack()