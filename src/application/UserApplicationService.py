"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.resource.exception.UserAlreadyExistException import UserAlreadyExistException
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceTypeConstant
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.resource.logging.logger import logger


class UserApplicationService:
    def __init__(self, userRepository: UserRepository, authzService: AuthorizationService):
        self._userRepository = userRepository
        self._authzService: AuthorizationService = authzService

    def createUser(self, id: str = '', name: str = '', password: str = '', objectOnly: bool = False, token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.WRITE.value,
                                            resourceType=ResourceTypeConstant.USER.value):
                self._userRepository.userByName(name=name)
                raise UserAlreadyExistException(name)
            else:
                raise UnAuthorizedException()
        except UserDoesNotExistException:
            logger.debug(
                f'[{UserApplicationService.createUser.__qualname__}] - with name: {name}, objectOnly: {objectOnly}')
            if objectOnly:
                return User.createFrom(name=name, password=password)
            else:
                user = User.createFrom(id=id, name=name, password=password, publishEvent=True)
                self._userRepository.createUser(user)
                return user

    def userByNameAndPassword(self, name: str, password: str):
        return self._userRepository.userByNameAndPassword(name=name, password=password)

    def userById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.USER.value):
            return self._userRepository.userById(id=id)
        else:
            raise UnAuthorizedException()

    def users(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '', order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.USER.value):
            return self._userRepository.usersByOwnedRoles(ownedRoles=ownedRoles,
                                                          resultFrom=resultFrom,
                                                          resultSize=resultSize,
                                                          order=order)
        else:
            raise UnAuthorizedException()

    def deleteUser(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        resourceType=ResourceTypeConstant.USER.value):
            user = self._userRepository.userById(id=id)
            self._userRepository.deleteUser(user)
        else:
            raise UnAuthorizedException()

    def updateUser(self, id: str, name: str = None, password: str = None, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        resourceType=ResourceTypeConstant.USER.value):
            user = self._userRepository.userById(id=id)
            user.update({'name': name, 'password': password})
            self._userRepository.updateUser(user)
        else:
            raise UnAuthorizedException()