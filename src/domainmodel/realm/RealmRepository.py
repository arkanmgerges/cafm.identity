"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domainmodel.realm.Realm import Realm


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