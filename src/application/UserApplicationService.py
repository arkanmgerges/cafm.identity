"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.resource.exception.UserAlreadyExistException import UserAlreadyExistException
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.resource.logging.logger import logger


class UserApplicationService:
    def __init__(self, userRepository: UserRepository):
        self._userRepository = userRepository

    def createObjectOnly(self, name: str, password: str):
        try:
            self._userRepository.userByName(name=name)
            raise UserAlreadyExistException(name=name)
        except UserDoesNotExistException:
            logger.debug(f'[{UserApplicationService.createObjectOnly.__qualname__}] - with name = {name}')
            return User.createFrom(name=name, password=password)

    def createUser(self, id: str, name: str, password: str):
        try:
            self._userRepository.userByName(name=name)
            raise UserAlreadyExistException(name=name)
        except UserDoesNotExistException:
            logger.debug(f'[{UserApplicationService.createUser.__qualname__}] - with name = {name}')
            user = User.createFrom(id=id, name=name, password=password, publishEvent=True)
            self._userRepository.createUser(user)
            return user

    def userByNameAndPassword(self, name: str, password: str):
        return self._userRepository.userByNameAndPassword(name=name, password=password)

    def userById(self, id: str):
        return self._userRepository.userById(id=id)

    def users(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[User]:
        return self._userRepository.usersByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom, resultSize=resultSize)
