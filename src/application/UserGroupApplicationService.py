"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository


class UserGroupApplicationService:
    def __init__(self, userGroupRepository: UserGroupRepository):
        self._userGroupRepository = userGroupRepository

    def createUserGroup(self, id: str = '', name: str = '', objectOnly: bool = False):
        try:
            self._userGroupRepository.userGroupByName(name=name)
            raise UserGroupAlreadyExistException(name=name)
        except UserGroupDoesNotExistException:
            if objectOnly:
                return UserGroup.createFrom(name=name)
            else:
                userGroup = UserGroup.createFrom(id=id, name=name, publishEvent=True)
                self._userGroupRepository.createUserGroup(userGroup)
                return userGroup

    def userGroupByName(self, name: str):
        return self._userGroupRepository.userGroupByName(name=name)

    def userGroupById(self, id: str):
        return self._userGroupRepository.userGroupById(id=id)

    def userGroups(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[UserGroup]:
        return self._userGroupRepository.userGroupsByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom, resultSize=resultSize)
