"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import RequestedAuthzObject
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import ResourceTypeContextDataRequest
from src.domain_model.token.TokenService import TokenService
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.domain_model.user.UserService import UserService


class UserApplicationService:
    def __init__(self, userRepository: UserRepository, authzService: AuthorizationService, userService: UserService):
        self._userRepository = userRepository
        self._authzService: AuthorizationService = authzService
        self._userService = userService

    def createUser(self, id: str = '', name: str = '', password:str = '', objectOnly: bool = False, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.CREATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='user'),
                                        tokenData=tokenData)
        return self._userService.createUser(id=id, name=name, password=password, objectOnly=objectOnly, tokenData=tokenData)

    def updateUser(self, id: str, name: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._userRepository.userById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.UPDATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='user'),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)
        self._userService.updateUser(oldObject=resource,
                                     newObject=User.createFrom(id=id, name=name), tokenData=tokenData)

    def deleteUser(self, id: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._userRepository.userById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.DELETE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='user'),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)
        self._userService.deleteUser(user=resource, tokenData=tokenData)

    def userByNameAndPassword(self, name: str, password: str):
        return self._userRepository.userByNameAndPassword(name=name, password=password)

    def userById(self, id: str, token: str = ''):
        resource = self._userRepository.userById(id=id)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessPermissionData,
                                        requestedPermissionAction=PermissionAction.READ,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.USER.value),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)

    def users(self, resultFrom: int = 0, resultSize: int = 100, token: str = '',
              order: List[dict] = None) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        return self._userRepository.users(tokenData=tokenData, roleAccessPermissionData=roleAccessPermissionData,
                                          resultFrom=resultFrom,
                                          resultSize=resultSize,
                                          order=order)
