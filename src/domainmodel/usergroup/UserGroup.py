"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class UserGroup:
    def __init__(self, id: str = str(uuid4())):
        self._id = id

    @classmethod
    def createNew(cls, id: str = str(uuid4())):
        from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
        from src.domainmodel.usergroup.UserGroupCreated import UserGroupCreated

        userGroup = UserGroup(id)
        DomainEventPublisher.addEventForPublishing(UserGroupCreated(userGroup))
        return userGroup

    @classmethod
    def createFrom(cls, id: str = str(uuid4())):
        return UserGroup(id)

    def id(self) -> str:
        return self._id

    def toMap(self) -> dict:
        return {"id": self.id()}
