"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domainmodel.resource.exception.UserAlreadyExistException import UserAlreadyExistException
from src.domainmodel.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domainmodel.user.User import User
from src.domainmodel.user.UserRepository import UserRepository


class UserApplicationService:
    def __init__(self, userRepository: UserRepository):
        self._userRepository = userRepository

    def createObjectOnly(self, username: str, password: str):
        try:
            self._userRepository.userByUsername(username=username)
            raise UserAlreadyExistException(username=username)
        except UserDoesNotExistException:
            return User.createFrom(username=username, password=password, publishEvent=False)

    def createUser(self, id: str, username: str, password: str):
        try:
            self._userRepository.userByUsername(username=username)
            raise UserAlreadyExistException(username=username)
        except UserDoesNotExistException:
            user = User.createFrom(id=id, username=username, password=password)
            self._userRepository.createUser(user)

    def userByUsernameAndPassword(self, username: str, password: str):
        return self._userRepository.userByUsernameAndPassword(username=username, password=password)
