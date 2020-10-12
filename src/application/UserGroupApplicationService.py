"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.PolicyControllerService import PolicyActionConstant
from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceTypeConstant
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository


class UserGroupApplicationService:
    def __init__(self, userGroupRepository: UserGroupRepository, authzService: AuthorizationService):
        self._userGroupRepository = userGroupRepository
        self._authzService: AuthorizationService = authzService

    def createUserGroup(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.WRITE.value,
                                            resourceType=ResourceTypeConstant.USER_GROUP.value):
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
        return self._userGroupRepository.userGroupsByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom,
                                                                resultSize=resultSize)
