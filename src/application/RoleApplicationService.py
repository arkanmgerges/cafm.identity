"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.PolicyControllerService import PolicyActionConstant
from src.domain_model.resource.exception.RoleAlreadyExistException import RoleAlreadyExistException
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.resource_type.ResourceType import ResourceTypeConstant
from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository


class RoleApplicationService:
    def __init__(self, roleRepository: RoleRepository, authzService: AuthorizationService):
        self._roleRepository = roleRepository
        self._authzService: AuthorizationService = authzService

    def createRole(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.WRITE.value,
                                            resourceType=ResourceTypeConstant.ROLE.value):
                self._roleRepository.roleByName(name=name)
                raise RoleAlreadyExistException(name=name)
            else:
                raise UnAuthorizedException()
        except RoleDoesNotExistException:
            if objectOnly:
                return Role.createFrom(name=name)
            else:
                role = Role.createFrom(id=id, name=name, publishEvent=True)
                self._roleRepository.createRole(role)
                return role

    def roleByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            return self._roleRepository.roleByName(name=name)
        else:
            raise UnAuthorizedException()

    def roleById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            return self._roleRepository.roleById(id=id)
        else:
            raise UnAuthorizedException()

    def deleteRole(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            role = self._roleRepository.roleById(id=id)
            self._roleRepository.deleteRole(role)
        else:
            raise UnAuthorizedException()

    def updateRole(self, id: str, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            role = self._roleRepository.roleById(id=id)
            role.update({'name': name})
            self._roleRepository.updateRole(role)
        else:
            raise UnAuthorizedException()

    def roles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '') -> List[Role]:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            return self._roleRepository.rolesByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom,
                                                          resultSize=resultSize)
        else:
            raise UnAuthorizedException()
