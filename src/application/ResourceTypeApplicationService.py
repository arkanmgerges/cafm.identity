"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceType
from src.domain_model.resource_type.ResourceTypeRepository import ResourceTypeRepository


class ResourceTypeApplicationService:
    def __init__(self, resourceTypeRepository: ResourceTypeRepository):
        self._resourceTypeRepository = resourceTypeRepository

    def createResourceType(self, id: str = '', name: str = '', objectOnly: bool = False):
        try:
            self._resourceTypeRepository.resourceTypeByName(name=name)
            raise ResourceTypeAlreadyExistException(name=name)
        except ResourceTypeDoesNotExistException:
            if objectOnly:
                return ResourceType.createFrom(name=name)
            else:
                resourceType = ResourceType.createFrom(id=id, name=name, publishEvent=True)
                self._resourceTypeRepository.createResourceType(resourceType)
                return resourceType

    def resourceTypeByName(self, name: str):
        return self._resourceTypeRepository.resourceTypeByName(name=name)

    def resourceTypeById(self, id: str):
        return self._resourceTypeRepository.resourceTypeById(id=id)

    def resourceTypes(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[ResourceType]:
        return self._resourceTypeRepository.resourceTypesByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom, resultSize=resultSize)
