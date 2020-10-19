"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.PolicyControllerService import PolicyActionConstant
from src.domain_model.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.resource_type.ResourceType import ResourceType, ResourceTypeConstant
from src.domain_model.resource_type.ResourceTypeRepository import ResourceTypeRepository


class ResourceTypeApplicationService:
    def __init__(self, resourceTypeRepository: ResourceTypeRepository, authzService: AuthorizationService):
        self._resourceTypeRepository = resourceTypeRepository
        self._authzService: AuthorizationService = authzService

    def createResourceType(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.WRITE.value,
                                            resourceType=ResourceTypeConstant.RESOURCE_TYPE.value):
                self._resourceTypeRepository.resourceTypeByName(name=name)
                raise ResourceTypeAlreadyExistException(name)
            else:
                raise UnAuthorizedException()
        except ResourceTypeDoesNotExistException:
            if objectOnly:
                return ResourceType.createFrom(name=name)
            else:
                resourceType = ResourceType.createFrom(id=id, name=name, publishEvent=True)
                self._resourceTypeRepository.createResourceType(resourceType)
                return resourceType

    def resourceTypeByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.RESOURCE_TYPE.value):
            return self._resourceTypeRepository.resourceTypeByName(name=name)
        else:
            raise UnAuthorizedException()

    def resourceTypeById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.RESOURCE_TYPE.value):
            return self._resourceTypeRepository.resourceTypeById(id=id)
        else:
            raise UnAuthorizedException()

    def resourceTypes(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '', order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.RESOURCE_TYPE.value):
            return self._resourceTypeRepository.resourceTypesByOwnedRoles(ownedRoles=ownedRoles,
                                                                          resultFrom=resultFrom,
                                                                          resultSize=resultSize,
                                                                          order=order)
        else:
            raise UnAuthorizedException()

    def deleteResourceType(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        resourceType=ResourceTypeConstant.RESOURCE_TYPE.value):
            resourceType = self._resourceTypeRepository.resourceTypeById(id=id)
            self._resourceTypeRepository.deleteResourceType(resourceType)
        else:
            raise UnAuthorizedException()

    def updateResourceType(self, id: str, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        resourceType=ResourceTypeConstant.RESOURCE_TYPE.value):
            resourceType = self._resourceTypeRepository.resourceTypeById(id=id)
            resourceType.update({'name': name})
            self._resourceTypeRepository.updateResourceType(resourceType)
        else:
            raise UnAuthorizedException()