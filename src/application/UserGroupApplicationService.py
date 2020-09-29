"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository


class UserGroupApplicationService:
    def __init__(self, userGroupRepository: UserGroupRepository):
        self._userGroupRepository = userGroupRepository

    def createObjectOnly(self, name: str):
        try:
            self._userGroupRepository.userGroupByName(name=name)
            raise UserGroupAlreadyExistException(name=name)
        except UserGroupDoesNotExistException:
            return UserGroup.createFrom(name=name, publishEvent=False)

    def createUserGroup(self, id: str, name: str):
        try:
            self._userGroupRepository.userGroupByName(name=name)
            raise UserGroupAlreadyExistException(name=name)
        except UserGroupDoesNotExistException:
            userGroup = UserGroup.createFrom(id=id, name=name)
            self._userGroupRepository.createUserGroup(userGroup)

    def userGroupByName(self, name: str):
        return self._userGroupRepository.userGroupByName(name=name)
