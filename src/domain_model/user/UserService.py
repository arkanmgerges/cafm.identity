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
    def createUser(self, id: str = '', name: str = '', password:str = '', firstName='', lastName='',
                   addressLineOne='', addressLineTwo='', postalCode='', avatarImage='', objectOnly: bool = False, tokenData: TokenData = None):
        try:
            if id == '':
                raise UserDoesNotExistException()
            self._repo.userByName(name=name)
            raise UserAlreadyExistException(name)
        except UserDoesNotExistException:
            if objectOnly:
                return User.createFrom(name=name, password=password, firstName=firstName,
                                       lastName=lastName, addressLineOne=addressLineOne, 
                                       addressLineTwo=addressLineTwo, postalCode=postalCode, 
                                       avatarImage=avatarImage)
            else:
                user = User.createFrom(id=id, name=name, password=password,  firstName=firstName,
                                       lastName=lastName, addressLineOne=addressLineOne, 
                                       addressLineTwo=addressLineTwo, postalCode=postalCode, 
                                       avatarImage=avatarImage, publishEvent=True)
                self._repo.createUser(user=user, tokenData=tokenData)
                return user

    @debugLogger
    def deleteUser(self, user: User, tokenData: TokenData = None):
        self._repo.deleteUser(user, tokenData=tokenData)
        user.publishDelete()

    @debugLogger
    def updateUser(self, oldObject: User, newObject: User, tokenData: TokenData = None):
        self._repo.updateUser(newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
