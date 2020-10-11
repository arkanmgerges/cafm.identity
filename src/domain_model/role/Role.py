"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Role:
    def __init__(self, id: str = str(uuid4()), name='', creator: str = 'super_admin'):
        self._id = id
        self._name = name
        self._creator = creator

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name='', publishEvent: bool = False, creator: str = 'super_admin'):
        role = Role(id, name, creator)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.role.RoleCreated import RoleCreated
            logger.debug(
                f'[{Role.createFrom.__qualname__}] - Create Role with name: {name} and id: {id}, creator: {creator}')
            DomainEventPublisher.addEventForPublishing(RoleCreated(role))
        return role

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}
