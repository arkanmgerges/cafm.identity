"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository


class UserGroupService:
    def __init__(self, userGroupRepo: UserGroupRepository, policyRepo: PolicyRepository):
        self._repo = userGroupRepo
        self._policyRepo = policyRepo

    def createUserGroup(self, id: str = '', name: str = '', objectOnly: bool = False, tokenData: TokenData = None):
        try:
            self._repo.userGroupByName(name=name)
            raise UserGroupAlreadyExistException(name)
        except UserGroupDoesNotExistException:
            if objectOnly:
                return UserGroup.createFrom(name=name)
            else:
                userGroup = UserGroup.createFrom(id=id, name=name, publishEvent=True)
                self._repo.createUserGroup(userGroup=userGroup, tokenData=tokenData)
                return userGroup

    def deleteUserGroup(self, userGroup: UserGroup, tokenData: TokenData = None):
        self._repo.deleteUserGroup(userGroup, tokenData=tokenData)
        userGroup.publishDelete()

    def updateUserGroup(self, oldObject: UserGroup, newObject: UserGroup, tokenData: TokenData = None):
        self._repo.updateUserGroup(newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
