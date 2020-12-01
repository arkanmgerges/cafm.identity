"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import RequestedAuthzObject
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import ResourceTypeContextDataRequest
from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository
from src.domain_model.realm.RealmService import RealmService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger


class RealmApplicationService:
    def __init__(self, realmRepository: RealmRepository, authzService: AuthorizationService,
                 realmService: RealmService):
        self._realmRepository = realmRepository
        self._authzService: AuthorizationService = authzService
        self._realmService = realmService

    @debugLogger
    def createRealm(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.CREATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='realm'),
                                        tokenData=tokenData)
        return self._realmService.createRealm(id=id, name=name, objectOnly=objectOnly, tokenData=tokenData)

    @debugLogger
    def updateRealm(self, id: str, name: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._realmRepository.realmById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.UPDATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='realm'),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)
        self._realmService.updateRealm(oldObject=resource,
                                       newObject=Realm.createFrom(id=id, name=name), tokenData=tokenData)

    @debugLogger
    def deleteRealm(self, id: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._realmRepository.realmById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.DELETE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='realm'),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)
        self._realmService.deleteRealm(realm=resource, tokenData=tokenData)

    @debugLogger
    def realmByName(self, name: str, token: str = ''):
        resource =  self._realmRepository.realmByName(name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessPermissionData,
                                        requestedPermissionAction=PermissionAction.READ,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.REALM.value),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)

    @debugLogger
    def realmById(self, id: str, token: str = ''):
        resource = self._realmRepository.realmById(id=id)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessPermissionData,
                                        requestedPermissionAction=PermissionAction.READ,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.REALM.value),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)

    @debugLogger
    def realms(self, resultFrom: int = 0, resultSize: int = 100, token: str = '',
               order: List[dict] = None) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        return self._realmRepository.realms(tokenData=tokenData, roleAccessPermissionData=roleAccessPermissionData,
                                      resultFrom=resultFrom,
                                      resultSize=resultSize,
                                      order=order)
