"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod


class HasToMap(ABC):
    @abstractmethod
    def toMap(self) -> dict:
        pass