"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.token.TokenData import TokenData
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.OuAlreadyExistException import OuAlreadyExistException
from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.resource.logging.decorator import debugLogger


class OuService:
    def __init__(self, ouRepo: OuRepository, policyRepo: PolicyRepository):
        self._repo = ouRepo
        self._policyRepo = policyRepo

    @debugLogger
    def createOu(self, obj: Ou, objectOnly: bool = False, tokenData: TokenData = None):
        if objectOnly:
            return Ou.createFromObject(obj=obj, generateNewId=True) if obj.id() == '' else obj
        else:
            obj = Ou.createFromObject(obj=obj, publishEvent=True)
            self._repo.save(obj=obj, tokenData=tokenData)
            return obj

    @debugLogger
    def deleteOu(self, obj:Ou, tokenData: TokenData = None):
        obj.publishDelete()
        self._repo.deleteOu(obj=obj, tokenData=tokenData)

    @debugLogger
    def updateOu(self, oldObject:Ou, newObject: Ou, tokenData: TokenData = None):
        newObject.publishUpdate(oldObject)
        self._repo.save(obj=newObject, tokenData=tokenData)
