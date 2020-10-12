"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.PolicyControllerService import PolicyActionConstant
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository
from src.domain_model.resource.exception.OuAlreadyExistException import OuAlreadyExistException
from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceTypeConstant


class OuApplicationService:
    def __init__(self, ouRepository: OuRepository, authzService: AuthorizationService):
        self._ouRepository = ouRepository
        self._authzService: AuthorizationService = authzService

    def createOu(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.WRITE.value,
                                            resourceType=ResourceTypeConstant.OU.value):
                self._ouRepository.ouByName(name=name)
                raise OuAlreadyExistException(name=name)
        except OuDoesNotExistException:
            if objectOnly:
                return Ou.createFrom(name=name)
            else:
                ou = Ou.createFrom(id=id, name=name, publishEvent=True)
                self._ouRepository.createOu(ou)
                return ou

    def ouByName(self, name: str):
        return self._ouRepository.ouByName(name=name)

    def ouById(self, id: str):
        return self._ouRepository.ouById(id=id)

    def ous(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Ou]:
        return self._ouRepository.ousByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom, resultSize=resultSize)
