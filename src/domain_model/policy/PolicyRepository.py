"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List, Any


class PolicyRepository(ABC):
    @abstractmethod
    def allTreeByRoleName(self, roleName: str) -> List[Any]:
        """Retrieve all the connection by role name

        Args:
            roleName (str): Role name that is used to retrieve the connected nodes to it

        """
