"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.realm.Realm import Realm


class RealmRepository(ABC):
    @abstractmethod
    def createRealm(self, realm: Realm):
        """Create realm

        Args:
            realm (Realm): The realm that needs to be created

        """

    @abstractmethod
    def realmByName(self, name: str) -> Realm:
        """Get realm by name

        Args:
            name (str): The name of the realm

        Returns:
            Realm: realm object
        """

    @abstractmethod
    def realmById(self, id: str) -> Realm:
        """Get realm by id

        Args:
            id (str): The id of the realm

        Returns:
            Realm: realm object
        """

    @abstractmethod
    def realmsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                           order: List[dict] = None) -> dict:
        """Get list of realms based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """

    @abstractmethod
    def deleteRealm(self, realm: Realm) -> None:
        """Delete a realm

        Args:
            realm (Realm): The realm that needs to be deleted
        """

    @abstractmethod
    def updateRealm(self, realm: Realm) -> None:
        """Update a realm

        Args:
            realm (Realm): The realm that needs to be updated
        """
