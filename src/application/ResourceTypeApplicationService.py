"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domainmodel.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
from src.domainmodel.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domainmodel.resourcetype.ResourceType import ResourceType
from src.domainmodel.resourcetype.ResourceTypeRepository import ResourceTypeRepository


class ResourceTypeApplicationService:
    def __init__(self, resourceTypeRepository: ResourceTypeRepository):
        self._resourceTypeRepository = resourceTypeRepository

    def createObjectOnly(self, name: str):
        try:
            self._resourceTypeRepository.resourceTypeByName(name=name)
            raise ResourceTypeAlreadyExistException(name=name)
        except ResourceTypeDoesNotExistException:
            return ResourceType.createFrom(name=name, publishEvent=False)

    def createResourceType(self, id: str, name: str):
        try:
            self._resourceTypeRepository.resourceTypeByName(name=name)
            raise ResourceTypeAlreadyExistException(name=name)
        except ResourceTypeDoesNotExistException:
            resourceType = ResourceType.createFrom(id=id, name=name)
            self._resourceTypeRepository.createResourceType(resourceType)

    def resourceTypeByName(self, name: str):
        return self._resourceTypeRepository.resourceTypeByName(name=name)
