"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

import authlib

from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.permission.Permission import PermissionAction, Permission
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant, PermissionContext
from src.domain_model.policy.AccessNode import AccessNode
from src.domain_model.policy.PermissionWithPermissionContexts import PermissionWithPermissionContexts
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ContextDataRequest import ContextDataRequestConstant, \
    ContextDataRequest
from src.domain_model.policy.request_context_data.ResourceInstanceContextDataRequest import \
    ResourceInstanceContextDataRequest
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import ResourceTypeContextDataRequest
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenData import TokenData
from src.resource.logging.logger import logger


class AuthorizationService:
    def __init__(self, authzRepo: AuthorizationRepository, policyService: PolicyControllerService):
        self._authzRepo = authzRepo
        self._policyService = policyService

    def isAllowed(self, token: str, action: str = '', permissionContext: str = '', resourceId: str = None) -> bool:
        """Authenticate user and return jwt token

        Args:
            token (str): Token that is used for authorization check
            action (str): An action that can be applied over the resource or/and permission context
            permissionContext (str): The type of the resource that the action will be applied to
            resourceId (str): The id of the resource that the action will be applied to

        Return:
            bool:
        """
        try:
            if not self._authzRepo.tokenExists(token=token):
                return False

            if not self._policyService.isAllowed(token=token):
                return False

            return True
        except authlib.jose.errors.BadSignatureError as e:
            logger.exception(
                f'[{AuthorizationService.isAllowed.__qualname__}] - exception raised for invalid token with e: {e}')
            return False
        except Exception as e:
            logger.exception(f'[{AuthorizationService.isAllowed.__qualname__}] - exception raised with e: {e}')
            raise e

    def roleAccessPermissionsData(self, tokenData: TokenData, includeAccessTree: bool = True):
        return self._policyService.roleAccessPermissionsData(tokenData=tokenData, includeAccessTree=includeAccessTree)

    def verifyAccess(self,
                     roleAccessPermissionsData: List[RoleAccessPermissionData],
                     requestedPermissionAction: PermissionAction,
                     requestedContextData: ContextDataRequest,
                     tokenData: TokenData,
                     resource: Resource = None):

        if not self._isSuperAdmin(tokenData=tokenData):
            if requestedPermissionAction in [PermissionAction.CREATE]:
                if self._verifyActionByPermissionWithPermissionContext(
                        requestedPermissionAction=requestedPermissionAction,
                        requestedContextData=requestedContextData,
                        roleAccessPermissionsData=roleAccessPermissionsData,
                        tokenData=tokenData,
                        resource=resource):
                    return
            if requestedPermissionAction in [PermissionAction.DELETE]:
                if self._verifyActionByPermissionWithPermissionContext(
                        requestedPermissionAction=requestedPermissionAction,
                        requestedContextData=requestedContextData,
                        roleAccessPermissionsData=roleAccessPermissionsData,
                        tokenData=tokenData,
                        resource=resource):
                    return
            if requestedPermissionAction in [PermissionAction.UPDATE]:
                if self._verifyActionByPermissionWithPermissionContext(
                        requestedPermissionAction=requestedPermissionAction,
                        requestedContextData=requestedContextData,
                        roleAccessPermissionsData=roleAccessPermissionsData,
                        tokenData=tokenData,
                        resource=resource):
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
                                                       resource: Resource) -> bool:
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
                            return self._checkForResourceTypeRequest(requestedPermissionAction, permissionContext,
                                                                     tokenData,
                                                                     item.accessTree,
                                                                     requestedContextData, resource)
                        # If it is requested to deal with resource instance?
                        if requestedContextData.dataType == ContextDataRequestConstant.RESOURCE_INSTANCE:
                            return self._checkForResourceInstanceRequest(requestedPermissionAction, permissionContext,
                                                                         tokenData,
                                                                         item.accessTree,
                                                                         requestedContextData, resource)
                    return False

        # We did not find action with permission context, then return false
        return False

    def _checkForResourceTypeRequest(self, requestedPermissionAction: PermissionAction,
                                     permissionContext: PermissionContext,
                                     tokenData: TokenData,
                                     accessTree: List[AccessNode],
                                     requestedContextData: ContextDataRequest, resource: Resource):
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
                    if requestedPermissionAction in [PermissionAction.READ, PermissionAction.UPDATE,
                                                     PermissionAction.DELETE]:
                        # Check if it is the owner
                        if self._policyService.isOwnerOfResource(resource=resource, tokenData=tokenData):
                            return True
                        # Check if the resource is in its access list
                        return self._treeCheck(accessTree, resource)



                        # Otherwise return False
                        return False
        return False

    def _checkForResourceInstanceRequest(self, requestedPermissionAction: PermissionAction,
                                         permissionContext: PermissionContext,
                                         tokenData: TokenData,
                                         accessTree: List[AccessNode],
                                         requestedContextData: ContextDataRequest, resource: Resource):
        resourceInstanceContextDataRequest: ResourceInstanceContextDataRequest = ResourceInstanceContextDataRequest.castFrom(
            requestedContextData)

        if requestedPermissionAction in [PermissionAction.READ, PermissionAction.UPDATE, PermissionAction.DELETE]:
            # Check if it is the owner
            if self._policyService.isOwnerOfResource(resource=resource, tokenData=tokenData):
                return True

        # Then check if the current type of the permission context is of type resource_type, and
        # if it is of resource type, then:
        if permissionContext.type() == PermissionContextConstant.RESOURCE_INSTANCE.value:
            # Get the data from the permission context
            data = permissionContext.data()
            # Check if it has the key 'name', and if it has, then:
            if 'name' in data:
                # Return true if the data context has a resource type requested that is the same
                # for data['name']
                if resourceInstanceContextDataRequest.resource.type() == data['name']:
                    return True
        return False

    def _isDeniedInstance(self) -> bool:
        return False

    def _treeCheck(self, accessTree: List[AccessNode], resource: Resource):
        for treeItem in accessTree:
            if self._isDeniedInstance():
                return False
            if treeItem.resource.type() == resource.type():
                return True
            if len(treeItem.children) > 0:



