"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.realm.Realm import Realm
from src.domain_model.token.TokenData import TokenData


class RealmRepository(ABC):
    @abstractmethod
    def save(self, obj: Realm, tokenData: TokenData):
        """Save realm

        Args:
            obj (Realm): The realm that needs to be saved
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def deleteRealm(self, obj: Realm, tokenData: TokenData) -> None:
        """Delete a realm

        Args:
            obj (Realm): The realm that needs to be deleted
            tokenData (TokenData): Token data used for deleting the resource

        :raises:
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the realm could not be deleted
        """

    @abstractmethod
    def realmByName(self, name: str) -> Realm:
        """Get realm by name

        Args:
            name (str): The name of the realm

        Returns:
            Realm: realm object

        :raises:
            `RealmDoesNotExistException <src.domain_model.resource.exception.RealmDoesNotExistException>` Raise an exception if the realm does not exist
        """

    @abstractmethod
    def realmById(self, id: str) -> Realm:
        """Get realm by id

        Args:
            id (str): The id of the realm

        Returns:
            Realm: realm object

        :raises:
            `RealmDoesNotExistException <src.domain_model.resource.exception.RealmDoesNotExistException>` Raise an exception if the realm does not exist
        """

    @abstractmethod
    def realms(
        self,
        tokenData: TokenData,
        roleAccessPermissionData: List[RoleAccessPermissionData],
        resultFrom: int = 0,
        resultSize: int = 100,
        order: List[dict] = None,
    ) -> dict:
        """Get list of realms based on the owned roles that the user has

        Args:
            tokenData (TokenData): A token data object
            roleAccessPermissionData (List[RoleAccessPermissionData]): List of role access permissions
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "totalItemCount": 0}
        """
