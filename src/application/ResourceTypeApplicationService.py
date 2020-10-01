"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceType
from src.domain_model.resource_type.ResourceTypeRepository import ResourceTypeRepository


class ResourceTypeApplicationService:
    def __init__(self, resourceTypeRepository: ResourceTypeRepository):
        self._resourceTypeRepository = resourceTypeRepository

    def createObjectOnly(self, name: str):
        try:
            self._resourceTypeRepository.resourceTypeByName(name=name)
            raise ResourceTypeAlreadyExistException(name=name)
        except ResourceTypeDoesNotExistException:
            return ResourceType.createFrom(name=name)

    def createResourceType(self, id: str, name: str):
        try:
            self._resourceTypeRepository.resourceTypeByName(name=name)
            raise ResourceTypeAlreadyExistException(name=name)
        except ResourceTypeDoesNotExistException:
            resourceType = ResourceType.createFrom(id=id, name=name, publishEvent=True)
            self._resourceTypeRepository.createResourceType(resourceType)

    def resourceTypeByName(self, name: str):
        return self._resourceTypeRepository.resourceTypeByName(name=name)
