"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository
from src.resource.logging.decorator import debugLogger


class UserGroupService:
    def __init__(self, userGroupRepo: UserGroupRepository, policyRepo: PolicyRepository):
        self._repo = userGroupRepo
        self._policyRepo = policyRepo

    @debugLogger
    def createUserGroup(self, obj: UserGroup, objectOnly: bool = False, tokenData: TokenData = None):
        try:
            if obj.id() == '':
                raise UserGroupDoesNotExistException()
            self._repo.userGroupByName(name=obj.name())
            raise UserGroupAlreadyExistException(obj.name())
        except UserGroupDoesNotExistException:
            if objectOnly:
                return UserGroup.createFromObject(obj=obj, generateNewId=True) if obj.id() == '' else obj
            else:
                obj = UserGroup.createFromObject(obj=obj, publishEvent=True)
                self._repo.createUserGroup(obj=obj, tokenData=tokenData)
                return obj

    @debugLogger
    def deleteUserGroup(self, obj: UserGroup, tokenData: TokenData = None):
        self._repo.deleteUserGroup(obj=obj, tokenData=tokenData)
        obj.publishDelete()

    @debugLogger
    def updateUserGroup(self, oldObject: UserGroup, newObject: UserGroup, tokenData: TokenData = None):
        self._repo.updateUserGroup(obj=newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
