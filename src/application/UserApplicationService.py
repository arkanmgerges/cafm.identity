"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import RequestedAuthzObject
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import (
    PermissionContextConstant,
)
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import (
    ResourceTypeContextDataRequest,
)
from src.domain_model.token.TokenService import TokenService
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.domain_model.user.UserService import UserService
from src.resource.logging.decorator import debugLogger


class UserApplicationService:
    def __init__(
        self,
        userRepository: UserRepository,
        authzService: AuthorizationService,
        userService: UserService,
    ):
        self._userRepository = userRepository
        self._authzService: AuthorizationService = authzService
        self._userService = userService

    @debugLogger
    def newId(self):
        return User.createFrom(skipValidation=True).id()

    @debugLogger
    def hasUserPasswordSet(self, userId: str) -> bool:
        user: User = self._userRepository.userById(userId)
        return not (user.hasOneTimePassword() or user.password() == "" or user.password() is None)

    @debugLogger
    def createUser(
        self, id: str = None, email: str = "", objectOnly: bool = False, token: str = ""
    ):
        obj: User = self.constructObject(id=id, email=email)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.CREATE,
            requestedContextData=ResourceTypeContextDataRequest(resourceType="user"),
            tokenData=tokenData,
        )
        return self._userService.createUser(
            obj=obj, objectOnly=objectOnly, tokenData=tokenData
        )

    @debugLogger
    def updateUser(self, id: str, email: str, token: str = ""):
        obj: User = self.constructObject(id=id, email=email)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        resource = self._userRepository.userById(id=obj.id())
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.UPDATE,
            requestedContextData=ResourceTypeContextDataRequest(resourceType="user"),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        self._userService.updateUser(
            oldObject=resource, newObject=obj, tokenData=tokenData
        )

    @debugLogger
    def deleteUser(self, id: str, token: str = "", **_kwargs):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        resource = self._userRepository.userById(id=id)
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.DELETE,
            requestedContextData=ResourceTypeContextDataRequest(resourceType="user"),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        self._userService.deleteUser(obj=resource, tokenData=tokenData)

    def deleteUserOneTimePassword(self, id: str, token: str = ""):
        tokenData = TokenService.tokenDataFromToken(token=token)
        resource = self._userRepository.userById(id=id)
        self._userRepository.deleteUserOneTimePassword(
            obj=resource, tokenData=tokenData
        )

    def setUserPassword(self, userId: str, password: str, token: str = ""):
        tokenData = TokenService.tokenDataFromToken(token=token)
        resource: User = self._userRepository.userById(id=userId)
        resource.setPassword(password=password)
        self._userRepository.setUserPassword(obj=resource, tokenData=tokenData)

    @debugLogger
    def userByEmailAndPassword(self, email: str, password: str):
        return self._userRepository.userByEmailAndPassword(
            email=email, password=password
        )

    @debugLogger
    def userById(self, id: str, token: str = ""):
        resource = self._userRepository.userById(id=id)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessPermissionData,
            requestedPermissionAction=PermissionAction.READ,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.USER.value
            ),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        return resource

    @debugLogger
    def users(
        self,
        resultFrom: int = 0,
        resultSize: int = 100,
        token: str = "",
        order: List[dict] = None,
    ) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        return self._userRepository.users(
            tokenData=tokenData,
            roleAccessPermissionData=roleAccessPermissionData,
            resultFrom=resultFrom,
            resultSize=resultSize,
            order=order,
        )

    def generateUserOneTimePassword(self, userId: str, token: str = "", **_kwargs):
        resource: User = self._userRepository.userById(id=userId)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessPermissionData,
            requestedPermissionAction=PermissionAction.READ,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.USER.value
            ),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        resource.generateOneTimePassword()
        self._userRepository.setUserPassword(resource, tokenData=tokenData)
        return resource

    @debugLogger
    def constructObject(
        self, id: str = None, email: str = "", password: str = ""
    ) -> User:
        return User.createFrom(id=id, email=email, password=password)
