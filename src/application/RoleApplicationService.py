"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.PolicyControllerService import PolicyActionConstant
from src.domain_model.resource.exception.RoleAlreadyExistException import RoleAlreadyExistException
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
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
        except RoleDoesNotExistException:
            if objectOnly:
                return Role.createFrom(name=name)
            else:
                role = Role.createFrom(id=id, name=name, publishEvent=True)
                self._roleRepository.createRole(role)
                return role

    def roleByName(self, name: str):
        return self._roleRepository.roleByName(name=name)

    def roleById(self, id: str):
        return self._roleRepository.roleById(id=id)

    def roles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Role]:
        return self._roleRepository.rolesByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom, resultSize=resultSize)
