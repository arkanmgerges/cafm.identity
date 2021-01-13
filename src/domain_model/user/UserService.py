"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.UserAlreadyExistException import UserAlreadyExistException
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.resource.logging.decorator import debugLogger


class UserService:
    def __init__(self, userRepo: UserRepository, policyRepo: PolicyRepository):
        self._repo = userRepo
        self._policyRepo = policyRepo

    @debugLogger
    def createUser(self, obj: User, objectOnly: bool = False, tokenData: TokenData = None):
        try:
            if obj.id() == '':
                raise UserDoesNotExistException()
            self._repo.userByEmail(email=obj.email())
            raise UserAlreadyExistException(obj.email())
        except UserDoesNotExistException:
            if objectOnly:
                return User.createFromObject(obj=obj, generateNewId=True) if obj.id() == '' else obj
            else:
                obj = User.createFromObject(obj=obj, publishEvent=True)
                self._repo.createUser(obj=obj, tokenData=tokenData)
                return obj

    @debugLogger
    def deleteUser(self, obj: User, tokenData: TokenData = None):
        self._repo.deleteUser(obj, tokenData=tokenData)
        obj.publishDelete()

    @debugLogger
    def updateUser(self, oldObject: User, newObject: User, tokenData: TokenData = None):
        self._repo.updateUser(obj=newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
