"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import RequestedAuthzObject
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository
from src.domain_model.ou.OuService import OuService
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import (
    PermissionContextConstant,
)
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import (
    ResourceTypeContextDataRequest,
)
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger


class OuApplicationService:
    def __init__(
        self,
        ouRepository: OuRepository,
        authzService: AuthorizationService,
        ouService: OuService,
    ):
        self._ouRepository = ouRepository
        self._authzService: AuthorizationService = authzService
        self._ouService = ouService

    @debugLogger
    def newId(self):
        return Ou.createFrom().id()

    @debugLogger
    def createOu(
        self,
        id: str = None,
        name: str = None,
        objectOnly: bool = False,
        token: str = "",
    ):
        obj: Ou = self.constructObject(id=id, name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.CREATE,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.OU.value
            ),
            tokenData=tokenData,
        )
        return self._ouService.createOu(
            obj=obj, objectOnly=objectOnly, tokenData=tokenData
        )

    @debugLogger
    def updateOu(self, id: str, name: str, token: str = ""):
        obj: Ou = self.constructObject(id=id, name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        resource = self._ouRepository.ouById(id=obj.id())
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.UPDATE,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.OU.value
            ),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        self._ouService.updateOu(oldObject=resource, newObject=obj, tokenData=tokenData)

    @debugLogger
    def deleteOu(self, id: str, token: str = ""):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        resource = self._ouRepository.ouById(id=id)
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.DELETE,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.OU.value
            ),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )

        self._ouService.deleteOu(obj=resource, tokenData=tokenData)

    @debugLogger
    def ouByName(self, name: str, token: str = ""):
        resource = self._ouRepository.ouByName(name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessPermissionData,
            requestedPermissionAction=PermissionAction.READ,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.OU.value
            ),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        return resource

    @debugLogger
    def ouById(self, id: str, token: str = ""):
        resource = self._ouRepository.ouById(id=id)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessPermissionData,
            requestedPermissionAction=PermissionAction.READ,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.OU.value
            ),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        return resource

    @debugLogger
    def ous(
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
        return self._ouRepository.ous(
            tokenData=tokenData,
            roleAccessPermissionData=roleAccessPermissionData,
            resultFrom=resultFrom,
            resultSize=resultSize,
            order=order,
        )

    @debugLogger
    def constructObject(self, id: str = None, name: str = None) -> Ou:
        return Ou.createFrom(id=id, name=name)
