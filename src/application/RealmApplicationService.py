"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant
from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository
from src.domain_model.resource.exception.RealmAlreadyExistException import RealmAlreadyExistException
from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant


class RealmApplicationService:
    def __init__(self, realmRepository: RealmRepository, authzService: AuthorizationService):
        self._realmRepository = realmRepository
        self._authzService: AuthorizationService = authzService

    def createRealm(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.WRITE.value,
                                            permissionContext=PermissionContextConstant.REALM.value):
                self._realmRepository.realmByName(name=name)
                raise RealmAlreadyExistException(name)
            else:
                raise UnAuthorizedException()
        except RealmDoesNotExistException:
            if objectOnly:
                return Realm.createFrom(name=name)
            else:
                realm = Realm.createFrom(id=id, name=name, publishEvent=True)
                self._realmRepository.createRealm(realm)
                return realm

    def realmByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.REALM.value):
            return self._realmRepository.realmByName(name=name)
        else:
            raise UnAuthorizedException()

    def realmById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.REALM.value):
            return self._realmRepository.realmById(id=id)
        else:
            raise UnAuthorizedException()

    def realms(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '', order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.REALM.value):
            return self._realmRepository.realmsByOwnedRoles(ownedRoles=ownedRoles,
                                                            resultFrom=resultFrom,
                                                            resultSize=resultSize,
                                                            order=order)
        else:
            raise UnAuthorizedException()

    def deleteRealm(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        permissionContext=PermissionContextConstant.REALM.value):
            realm = self._realmRepository.realmById(id=id)
            self._realmRepository.deleteRealm(realm)
        else:
            raise UnAuthorizedException()

    def updateRealm(self, id: str, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        permissionContext=PermissionContextConstant.REALM.value):
            realm = self._realmRepository.realmById(id=id)
            realm.update({'name': name})
            self._realmRepository.updateRealm(realm)
        else:
            raise UnAuthorizedException()