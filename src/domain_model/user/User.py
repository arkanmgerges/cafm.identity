"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import re
from copy import copy
from uuid import uuid4

from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.InvalidValueException import InvalidValueException
from src.resource.logging.logger import logger


class User(Resource):
    ONE_TIME_PASSWORD_TAG = '###ABC_ZYX_1_TIME_PASS'

    def __init__(self, id: str = None, email: str = '', password: str = '', firstName: str = '', lastName: str = '',
                 addressOne: str = '', addressTwo: str = '', postalCode: str = '', avatarImage: str = ''):
        anId = str(uuid4()) if id is None or id == '' else id
        super().__init__(id=anId, type='user')

        self._validateEmail(email)
        self._email = email
        self._password = password
        self._firstName = firstName
        self._lastName = lastName
        self._addressOne = addressOne
        self._addressTwo = addressTwo
        self._postalCode = postalCode
        self._avatarImage = avatarImage

    @classmethod
    def createFrom(cls, id: str = None, email: str = '', password: str = '', firstName: str = '', lastName: str = '',
                   addressOne: str = '', addressTwo: str = '', postalCode: str = '', avatarImage: str = '',
                   publishEvent: bool = False):
        logger.debug(f'[{User.createFrom.__qualname__}] - with name {email}')
        user = User(id=id, email=email, password=password, firstName=firstName, lastName=lastName,
                    addressOne=addressOne, addressTwo=addressTwo, postalCode=postalCode, avatarImage=avatarImage)
        if publishEvent:
            logger.debug(f'[{User.createFrom.__qualname__}] - publish UserCreated event')
            from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
            from src.domain_model.user.UserCreated import UserCreated
            DomainPublishedEvents.addEventForPublishing(UserCreated(user))
        return user

    def _validateEmail(self, email):
        regex = r'^[a-zA-Z0-9]+[a-zA-Z0-9\._]+[@]\w+[.]\w{2,6}$'
        if not (re.search(regex, email)):
            raise InvalidValueException(f'Email is not valid: {email}')

    def email(self) -> str:
        return self._email

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
        if 'email' in data and data['email'] != self._email and data['email'] is not None:
            updated = True
            self._email = data['name']
        if 'password' in data and data['password'] != self._password and data['password'] is not None:
            updated = True
            self._password = data['password']
        if 'first_name' in data and data['first_name'] != self._firstName and data['first_name'] is not None:
            updated = True
            self._firstName = data['first_name']
        if 'last_name' in data and data['last_name'] != self._lastName and data['last_name'] is not None:
            updated = True
            self._lastName = data['last_name']
        if 'address_one' in data and data['address_one'] != self._addressOne and data['address_one'] is not None:
            updated = True
            self._addressOne = data['address_one']
        if 'address_two' in data and data['address_two'] != self._addressTwo and data['address_two'] is not None:
            updated = True
            self._addressTwo = data['address_two']
        if 'postal_code' in data and data['postal_code'] != self._postalCode and data['postal_code'] is not None:
            updated = True
            self._postalCode = data['postal_code']
        if 'avatar_image' in data and data['avatar_image'] != self._avatarImage and data['avatar_image'] is not None:
            updated = True
            self._avatarImage = data['avatar_image']
        if updated:
            self.publishUpdate(old)

    def setPassword(self, password: str):
        from src.domain_model.user.UserPasswordSet import UserPasswordSet
        self._password = password
        DomainPublishedEvents.addEventForPublishing(UserPasswordSet(self))

    def password(self) -> str:
        return self._password

    def generateOneTimePassword(self):
        from src.domain_model.user.UserOneTimePasswordGenerated import UserOneTimePasswordGenerated
        self._password = f'{str(uuid4()).replace("-", "")}{User.ONE_TIME_PASSWORD_TAG}'
        DomainPublishedEvents.addEventForPublishing(UserOneTimePasswordGenerated(self))

    def isPasswordOneTimePassword(self):
        return self._password.endswith(User.ONE_TIME_PASSWORD_TAG)

    def stripOneTimePasswordTag(self):
        return self._password.replace(User.ONE_TIME_PASSWORD_TAG, '')

    def publishDelete(self):
        from src.domain_model.user.UserDeleted import UserDeleted
        DomainPublishedEvents.addEventForPublishing(UserDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.user.UserUpdated import UserUpdated
        DomainPublishedEvents.addEventForPublishing(UserUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "email": self.email(),
                "first_name": self.firstName(), "last_name": self.lastName(), "address_one": self.addressOne(),
                "address_two": self.addressTwo(), "postal_code": self.postalCode(), "avatar_image": self.avatarImage()}

    def __repr__(self):
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __str__(self) -> str:
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __eq__(self, other):
        if not isinstance(other, User):
            raise NotImplementedError(f'other: {other} can not be compared with User class')
        return self.id() == other.id() and self.email() == other.email() and \
               self.password() == other.password() and self.firstName() == other.firstName() and \
               self.lastName() == other.lastName() and self.addressOne() == other.addressOne() and \
               self.addressTwo() == other.addressTwo() and self.postalCode() == other.postalCode() and \
               self.avatarImage() == other.avatarImage()


