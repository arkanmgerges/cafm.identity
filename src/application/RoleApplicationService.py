"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domainmodel.resource.exception.RoleAlreadyExistException import RoleAlreadyExistException
from src.domainmodel.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domainmodel.role.Role import Role
from src.domainmodel.role.RoleRepository import RoleRepository


class RoleApplicationService:
    def __init__(self, roleRepository: RoleRepository):
        self._roleRepository = roleRepository

    def createObjectOnly(self, name: str):
        try:
            self._roleRepository.roleByName(name=name)
            raise RoleAlreadyExistException(name=name)
        except RoleDoesNotExistException:
            return Role.createFrom(name=name, publishEvent=False)

    def createRole(self, id: str, name: str):
        try:
            self._roleRepository.roleByName(name=name)
            raise RoleAlreadyExistException(name=name)
        except RoleDoesNotExistException:
            role = Role.createFrom(id=id, name=name)
            self._roleRepository.createRole(role)

    def roleByName(self, name: str):
        return self._roleRepository.roleByName(name=name)
