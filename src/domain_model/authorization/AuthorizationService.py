"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.RequestedAuthzObject import RequestedAuthzObject, RequestedAuthzObjectEnum
from src.domain_model.permission.Permission import PermissionAction, Permission
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant, PermissionContext
from src.domain_model.policy.AccessNode import AccessNode
from src.domain_model.policy.PermissionWithPermissionContexts import PermissionWithPermissionContexts
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ContextDataRequest import ContextDataRequestConstant, \
    ContextDataRequest
from src.domain_model.policy.request_context_data.PermissionContextDataRequest import PermissionContextDataRequest
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import ResourceTypeContextDataRequest
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenData import TokenData


class AuthorizationService:
    def __init__(self, authzRepo: AuthorizationRepository, policyService: PolicyControllerService):
        self._deniedResourcesWithActions = {}
        self._authzRepo = authzRepo
        self._policyService = policyService

    def roleAccessPermissionsData(self, tokenData: TokenData, includeAccessTree: bool = True) -> List[
        RoleAccessPermissionData]:
        return self._policyService.roleAccessPermissionsData(tokenData=tokenData, includeAccessTree=includeAccessTree)

    def verifyAccess(self,
                     roleAccessPermissionsData: List[RoleAccessPermissionData],
                     requestedPermissionAction: PermissionAction,
                     requestedContextData: ContextDataRequest,
                     tokenData: TokenData,
                     requestedObject: RequestedAuthzObject = None):

        if not self._isSuperAdmin(tokenData=tokenData):
            if requestedPermissionAction in [PermissionAction.READ]:
                if self._verifyActionByPermissionWithPermissionContext(
                        requestedPermissionAction=requestedPermissionAction,
                        requestedContextData=requestedContextData,
                        roleAccessPermissionsData=roleAccessPermissionsData,
                        tokenData=tokenData,
                        requestedObject=requestedObject):
                    return
            if requestedPermissionAction in [PermissionAction.CREATE]:
                if self._verifyActionByPermissionWithPermissionContext(
                        requestedPermissionAction=requestedPermissionAction,
                        requestedContextData=requestedContextData,
                        roleAccessPermissionsData=roleAccessPermissionsData,
                        tokenData=tokenData,
                        requestedObject=requestedObject):
                    return
            if requestedPermissionAction in [PermissionAction.DELETE]:
                if self._verifyActionByPermissionWithPermissionContext(
                        requestedPermissionAction=requestedPermissionAction,
                        requestedContextData=requestedContextData,
                        roleAccessPermissionsData=roleAccessPermissionsData,
                        tokenData=tokenData,
                        requestedObject=requestedObject):
                    return
            if requestedPermissionAction in [PermissionAction.UPDATE]:
                if self._verifyActionByPermissionWithPermissionContext(
                        requestedPermissionAction=requestedPermissionAction,
                        requestedContextData=requestedContextData,
                        roleAccessPermissionsData=roleAccessPermissionsData,
                        tokenData=tokenData,
                        requestedObject=requestedObject):
                    return

            # By default the access is forbidden
            raise UnAuthorizedException()

    def _isSuperAdmin(self, tokenData) -> bool:
        for role in tokenData.roles():
            if role['name'] == 'super_admin':
                return True
        return False

    def _verifyActionByPermissionWithPermissionContext(self, requestedPermissionAction: PermissionAction,
                                                       requestedContextData: ContextDataRequest,
                                                       roleAccessPermissionsData: List[
                                                           RoleAccessPermissionData],
                                                       tokenData: TokenData,
                                                       requestedObject: RequestedAuthzObject) -> bool:
        self._populateDeniedResources(roleAccessPermissionsData)
        for item in roleAccessPermissionsData:
            permissionsWithPermissionContexts: List[PermissionWithPermissionContexts] = item.permissions
            for permissionWithPermissionContexts in permissionsWithPermissionContexts:
                # If we find a permission with the 'action' for 'permission context' then return true
                permission: Permission = permissionWithPermissionContexts.permission
                permissionContexts: List[PermissionContext] = permissionWithPermissionContexts.permissionContexts
                # Does it have a permission action in the allowed actions?
                if requestedPermissionAction.value in permission.allowedActions():
                    # If yes, then check if we can find a permission context type that is similar to the
                    # permission context constant
                    for permissionContext in permissionContexts:
                        # If it is requested to deal with resource type?
                        if requestedContextData.dataType == ContextDataRequestConstant.RESOURCE_TYPE:
                            if self._checkForResourceTypeRequest(requestedPermissionAction, permissionContext,
                                                                 tokenData,
                                                                 item.accessTree,
                                                                 item.ownerOf,
                                                                 requestedContextData, requestedObject):
                                return True
                        if requestedContextData.dataType == ContextDataRequestConstant.PERMISSION:
                            reqObject: PermissionContextDataRequest = PermissionContextDataRequest.castFrom(
                                requestedContextData)
                            if reqObject.type == PermissionContextConstant.PERMISSION and \
                                    permissionContext.type() == PermissionContextConstant.PERMISSION:
                                return True
                            if reqObject.type == PermissionContextConstant.PERMISSION_CONTEXT and \
                                    permissionContext.type() == PermissionContextConstant.PERMISSION_CONTEXT:
                                return True

        # We did not find action with permission context, then return false
        return False

    def _checkForResourceTypeRequest(self, requestedPermissionAction: PermissionAction,
                                     permissionContext: PermissionContext,
                                     tokenData: TokenData,
                                     accessTree: List[AccessNode],
                                     ownerOf: List[Resource],
                                     requestedContextData: ContextDataRequest, requestedObject: RequestedAuthzObject):
        resourceTypeContextDataRequest: ResourceTypeContextDataRequest = ResourceTypeContextDataRequest.castFrom(
            requestedContextData)

        # Then check if the current type of the permission context is of type resource_type, and
        # if it is of resource type, then:
        if permissionContext.type() == PermissionContextConstant.RESOURCE_TYPE.value:
            # Get the data from the permission context
            data = permissionContext.data()
            # Check if it has the key 'name', and if it has, then:
            if 'name' in data:
                # Return true if the data context has a resource type requested that is the same
                # for data['name']
                if resourceTypeContextDataRequest.resourceType == data['name']:
                    # If permission action is other than CREATE, then:
                    if requestedPermissionAction in [PermissionAction.READ, PermissionAction.UPDATE,
                                                     PermissionAction.DELETE]:
                        if requestedObject.type == RequestedAuthzObjectEnum.RESOURCE:
                            for ownerItem in ownerOf:
                                if requestedObject.obj.id() == ownerItem.id():
                                    return True
                            # # Check if it is the owner of the resource, and if it is then return True
                            # if self._policyService.isOwnerOfResource(resource=requestedObject.obj, tokenData=tokenData):
                            #     return True

                            # Check if the resource is accessible in the tree
                            if self._isDeniedInstance(requestedObject.obj, requestedPermissionAction):
                                return False
                            return self._treeCheck(accessTree, requestedObject.obj, requestedPermissionAction)
                    elif requestedPermissionAction == PermissionAction.CREATE:
                        # If it is create
                        return True

        return False

    def _treeCheck(self, accessTree: List[AccessNode], requestedResource: Resource,
                   requestedPermissionAction: PermissionAction) -> bool:
        for treeItem in accessTree:
            # Get the current resource from the tree
            currentResource = treeItem.resource
            # Check if the user/role has read access to it
            if self._isDeniedInstance(currentResource, PermissionAction.READ):
                return False
            # Check if the current resource is the same as the requested resource
            if currentResource.id() == requestedResource.id():
                return True
            # Parse the children
            if len(treeItem.children) > 0:
                result = self._treeCheck(treeItem.children, requestedResource, requestedPermissionAction)
                if result is True:
                    return True
            return False

    def _isDeniedInstance(self, resource: Resource, requestedPermissionAction: PermissionAction) -> bool:
        id = resource.id()
        if id in self._deniedResourcesWithActions:
            actions = self._deniedResourcesWithActions[id]
            if requestedPermissionAction.value in actions:
                return True
        return False

    def _populateDeniedResources(self, roleAccessPermissionsData: List[
        RoleAccessPermissionData]):
        for item in roleAccessPermissionsData:
            for permissionWithPermissionContexts in item.permissions:
                permission = permissionWithPermissionContexts.permission
                for action in permission.deniedActions():
                    for permContext in permissionWithPermissionContexts.permissionContexts:
                        if permContext.type() == PermissionContextConstant.RESOURCE_INSTANCE:
                            id = permContext.id()
                            if id in self._deniedResourcesWithActions:
                                self._deniedResourcesWithActions[id].append(action)
                            else:
                                self._deniedResourcesWithActions[id] = []
                                self._deniedResourcesWithActions[id].append(action)
