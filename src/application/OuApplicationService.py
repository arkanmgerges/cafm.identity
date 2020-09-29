"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.OuAlreadyExistException import OuAlreadyExistException
from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository


class OuApplicationService:
    def __init__(self, ouRepository: OuRepository):
        self._ouRepository = ouRepository

    def createObjectOnly(self, name: str):
        try:
            self._ouRepository.ouByName(name=name)
            raise OuAlreadyExistException(name=name)
        except OuDoesNotExistException:
            return Ou.createFrom(name=name, publishEvent=False)

    def createOu(self, id: str, name: str):
        try:
            self._ouRepository.ouByName(name=name)
            raise OuAlreadyExistException(name=name)
        except OuDoesNotExistException:
            ou = Ou.createFrom(id=id, name=name)
            self._ouRepository.createOu(ou)

    def ouByName(self, name: str):
        return self._ouRepository.ouByName(name=name)
