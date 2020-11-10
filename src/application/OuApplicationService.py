"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.ou.OuRepository import OuRepository
from src.domain_model.ou.OuService import OuService
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import \
    ResourceInstanceContextDataRequest
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.token.TokenService import TokenService


class OuApplicationService:
    def __init__(self, ouRepository: OuRepository, authzService: AuthorizationService, ouService: OuService):
        self._ouRepository = ouRepository
        self._authzService: AuthorizationService = authzService
        self._ouService = ouService

    def createOu(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.CREATE,
                                        requestedContextData=ResourceInstanceContextDataRequest(resourceType='ou'),
                                        tokenData=tokenData)
        return self._ouService.createOu(id=id, name=name, objectOnly=objectOnly, tokenData=tokenData)

    def ouByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.OU.value):
            return self._ouRepository.ouByName(name=name)

    def ouById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.OU.value):
            return self._ouRepository.ouById(id=id)
        else:
            raise UnAuthorizedException()

    def ous(self, resultFrom: int = 0, resultSize: int = 100, token: str = '',
            order: List[dict] = None) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        return self._ouRepository.ousByOwnedRoles(tokenData=tokenData, resultFrom=resultFrom,
                                                  resultSize=resultSize,
                                                  order=order)
        # if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
        #                                 permissionContext=PermissionContextConstant.OU.value):
        #
        # else:
        #     raise UnAuthorizedException()

    def deleteOu(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        permissionContext=PermissionContextConstant.OU.value):
            ou = self._ouRepository.ouById(id=id)
            self._ouRepository.deleteOu(ou)
        else:
            raise UnAuthorizedException()

    def updateOu(self, id: str, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        permissionContext=PermissionContextConstant.OU.value):
            ou = self._ouRepository.ouById(id=id)
            ou.update({'name': name})
            self._ouRepository.updateOu(ou)
        else:
            raise UnAuthorizedException()
