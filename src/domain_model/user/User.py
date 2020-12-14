"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.resource.logging.logger import logger


class User(Resource):
    def __init__(self, id: str = None, name='', password='', firstName='', lastName='',
                 addressOne='', addressTwo='', postalCode='', avatarImage=''):
        anId = str(uuid4()) if id is None or id == '' else id
        super().__init__(id=anId, type='user')
        self._name = name
        self._password = password
        self._firstName = firstName
        self._lastName = lastName
        self._addressOne = addressOne
        self._addressTwo = addressTwo
        self._postalCode = postalCode
        self._avatarImage = avatarImage

    @classmethod
    def createFrom(cls, id: str = None, name='', password='', firstName='', lastName='',
                 addressOne='', addressTwo='', postalCode='', avatarImage='', publishEvent: bool = False):
        logger.debug(f'[{User.createFrom.__qualname__}] - with name {name}')
        user = User(id, name, password, firstName, lastName,
                    addressOne, addressTwo, postalCode, avatarImage)
        if publishEvent:
            logger.debug(f'[{User.createFrom.__qualname__}] - publish UserCreated event')
            from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
            from src.domain_model.user.UserCreated import UserCreated
            DomainPublishedEvents.addEventForPublishing(UserCreated(user))
        return user

    def name(self) -> str:
        return self._name
    
    def firstName(self) -> str:
        return self._firstName
    
    def lastName(self) -> str:
        return self._lastName
    
    def addressOne(self) -> str:
        return self._addressOne
    
    def addressTwo(self) -> str:
        return self._addressTwo
    
    def postalCode(self) -> str:
        return self._postalCode
    
    def avatarImage(self) -> str:
        return self._avatarImage

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if 'name' in data and data['name'] != self._name and data['name'] is not None:
            updated = True
            self._name = data['name']
        if 'password' in data and data['password'] != self._password and data['password'] is not None:
            updated = True
            self._password = data['password']
        if updated:
            self.publishUpdate(old)

    def password(self) -> str:
        return self._password

    def publishDelete(self):
        from src.domain_model.user.UserDeleted import UserDeleted
        DomainPublishedEvents.addEventForPublishing(UserDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.user.UserUpdated import UserUpdated
        DomainPublishedEvents.addEventForPublishing(UserUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name(),
                "first_name": self.firstName(), "last_name": self.lastName(), "address_one": self.addressOne(),
                "address_two": self.addressTwo(), "postal_code": self.postalCode(), "avatar_image": self.avatarImage()}

    def __eq__(self, other):
        if not isinstance(other, User):
            raise NotImplementedError(f'other: {other} can not be compared with User class')
        return self.id() == other.id() and self.name() == other.name() and self.firstName() == other.firstName() and \
               self.lastName() == other.lastName() and self.addressOne() == other.addressOne() and self.addressTwo() == other.addressTwo() and \
               self.postalCode() == other.postalCode() and self.avatarImage() == other.avatarImage()
