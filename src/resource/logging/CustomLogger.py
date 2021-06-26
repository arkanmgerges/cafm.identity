import os
import sys
from enum import Enum
from logging import Logger
from types import TracebackType
from typing import Text, Union, Any, Optional, Dict, Tuple

_SysExcInfoType = Union[
    Tuple[type, BaseException, Optional[TracebackType]], Tuple[None, None, None]
]


class LogLevelEnum(Enum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


def logLevelEnumItemFromString(logLevel: str):
    for logLevelEnumItem in LogLevelEnum:
        if logLevelEnumItem.name == logLevel:
            return logLevelEnumItem
    return LogLevelEnum.NOTSET


if sys.version_info >= (3, 5):
    _ExcInfoType = Union[None, bool, _SysExcInfoType, BaseException]
else:
    _ExcInfoType = Union[None, bool, _SysExcInfoType]


class CustomLogger(Logger):
    def __init__(self, name: str, level: Union[int, Text] = 0):
        super().__init__(name, level)

    def debug(
        self,
        msg: Any,
        *args: Any,
        exc_info: _ExcInfoType = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Optional[Dict[str, Any]] = ...,
        **kwargs: Any,
    ) -> None:
        self.modifyMsg(super().debug, msg)

    def info(
        self,
        msg: Any,
        *args: Any,
        excInfo: _ExcInfoType = ...,
        stackInfo: bool = False,
        stackLevel: int = 0,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        self.modifyMsg(super().info, msg)

    def warning(
        self,
        msg: Any,
        *args: Any,
        exc_info: _ExcInfoType = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Optional[Dict[str, Any]] = ...,
        **kwargs: Any,
    ) -> None:
        self.modifyMsg(super().warning, msg)

    def warn(
        self,
        msg: Any,
        *args: Any,
        exc_info: _ExcInfoType = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Optional[Dict[str, Any]] = ...,
        **kwargs: Any,
    ) -> None:
        self.modifyMsg(super().warn, msg)

    def error(
        self,
        msg: Any,
        *args: Any,
        exc_info: _ExcInfoType = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Optional[Dict[str, Any]] = ...,
        **kwargs: Any,
    ) -> None:
        self.modifyMsg(super().error, msg)

    def exception(
        self,
        msg: Any,
        *args: Any,
        exc_info: _ExcInfoType = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Optional[Dict[str, Any]] = ...,
        **kwargs: Any,
    ) -> None:
        self.modifyMsg(super().exception, msg)

    def critical(
        self,
        msg: Any,
        *args: Any,
        exc_info: _ExcInfoType = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Optional[Dict[str, Any]] = ...,
        **kwargs: Any,
    ) -> None:
        self.modifyMsg(super().critical, msg)

    def log(
        self,
        level: int,
        msg: Any,
        *args: Any,
        exc_info: _ExcInfoType = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Optional[Dict[str, Any]] = ...,
        **kwargs: Any,
    ) -> None:
        self.modifyMsg(super().log, msg)

    def modifyMsg(self, call, msg):
        maxLines = int(os.getenv("CAFM_IDENTITY_LOGGING_MAX_FILE_LINES", 5))
        modifiedMsgArray = []
        frame = sys._getframe()
        for frameIdx in range(0, maxLines):
            frame = frame.f_back
            callerModule = frame.f_globals["__name__"]
            callerName = frame.f_code.co_name
            lineNumber = frame.f_lineno
            fileName = frame.f_code.co_filename
            modifiedMsgArray.insert(0, f"\t[{callerModule}.{callerName}][file name: {fileName}][line number: {lineNumber}]\n")
        modifiedMsgArray.insert(0, "\nfiles:\n")
        modifiedMsgArray.append(f"message:\n \t{msg}")
        call("".join(modifiedMsgArray))

