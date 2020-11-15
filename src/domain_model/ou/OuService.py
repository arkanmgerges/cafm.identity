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


class OuService:
    def __init__(self, ouRepo: OuRepository, policyRepo: PolicyRepository):
        self._repo = ouRepo
        self._policyRepo = policyRepo

    def createOu(self, id: str = '', name: str = '', objectOnly: bool = False, tokenData: TokenData = None):
        try:
            self._repo.ouByName(name=name)
            raise OuAlreadyExistException(name)
        except OuDoesNotExistException:
            if objectOnly:
                return Ou.createFrom(name=name)
            else:
                ou = Ou.createFrom(id=id, name=name, publishEvent=True)
                self._repo.createOu(ou=ou, tokenData=tokenData)
                # self._policyRepo.connectResourceToOwner(
                #     resource=Resource(
                #         id=ou.id(),
                #         type=PermissionContextConstant.OU.value),
                #     tokenData=tokenData)
                return ou

    def deleteOu(self, ou:Ou, tokenData: TokenData = None):
        self._repo.deleteOu(ou, tokenData=tokenData)
        ou.publishDelete()

    def updateOu(self, ou:Ou, tokenData: TokenData = None):
        self._repo.updateOu(ou, tokenData=tokenData)
        ou.publishDelete()
