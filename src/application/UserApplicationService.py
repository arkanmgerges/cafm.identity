"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.UserAlreadyExistException import UserAlreadyExistException
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.resource.logging.logger import logger


class UserApplicationService:
    def __init__(self, userRepository: UserRepository):
        self._userRepository = userRepository

    def createObjectOnly(self, username: str, password: str):
        try:
            self._userRepository.userByUsername(username=username)
            raise UserAlreadyExistException(username=username)
        except UserDoesNotExistException:
            logger.debug(f'[{UserApplicationService.createObjectOnly.__qualname__}] - with name = {username}')
            return User.createFrom(username=username, password=password, publishEvent=False)

    def createUser(self, id: str, username: str, password: str):
        try:
            self._userRepository.userByUsername(username=username)
            raise UserAlreadyExistException(username=username)
        except UserDoesNotExistException:
            logger.debug(f'[{UserApplicationService.createUser.__qualname__}] - with name = {username}')
            user = User.createFrom(id=id, username=username, password=password)
            self._userRepository.createUser(user)
            return user

    def userByUsernameAndPassword(self, username: str, password: str):
        return self._userRepository.userByUsernameAndPassword(username=username, password=password)
