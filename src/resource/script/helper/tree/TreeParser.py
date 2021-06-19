from typing import List

import click

from src.resource.script.helper.cache.Cache import Cache


class TreeParser:
    def __init__(self, cafmClient):
        self._cafmClient = cafmClient

    # region Resource Tree
    def parseResourceTree(self, parent):
        """Parses the tree nodes and creates resources by node type
        Args:
            parent (obj): The parent node containing 'resource_type', 'resource_name', 'children' and other fields
        """

        if parent is None:
            return

        resource = self.ensureResourceExistence(parent)
        if resource is None:
            raise Exception(f"Something went wrong while ensuring resource existence for node {parent}")

        for child in parent["children"]:
            childResource = self.parseResourceTree(child)
            if childResource is not None:
                self.ensureAssignmentFromParentResourceToChildResourceExistence(parent=resource, child=childResource)

        return resource

    def ensureAssignmentFromParentResourceToChildResourceExistence(self, parent, child):
        self._cafmClient.createAssignmentResourceToResource(fromId=parent["id"], toId=child["id"], ignoreExistence=True)

    def ensureResourceExistence(self, node):
        """Create or update the resource according to the node type
        Args:
            node (obj): The node containing 'type', 'name' / 'email', 'realm_type', 'title'
        Returns an object containing the resource id of the node
        """

        if node["resource_type"] == "realm":
            resourceId = self._cafmClient.ensureRealmExistence(name=node["name"], realmType=node["realm_type"])
            node["id"] = resourceId
            return node
        if node["resource_type"] == "ou":
            resourceId = self._cafmClient.ensureOuExistence(name=node["name"])
            node["id"] = resourceId
            return node
        if node["resource_type"] == "project":
            resourceId = self._cafmClient.ensureProjectExistence(name=node["name"])
            node["id"] = resourceId
            return node

    # endregion Resource Tree

    # region Permission Tree
    def parsePermissionTree(self, parent):
        existingPermissions = self._cafmClient.readPermissions()
        if parent["tree_type"] == "collection":
            permissions = self.parsePermissionsCollection(
                newPermissionsNames=parent["children"],
                currentPermissions=existingPermissions,
            )
            parent["permissions"] = permissions
            return parent

        if parent["tree_type"] == "aggregation":
            permissions = self.parsePermissionsAggregation(
                permissionTrees=parent["children"],
                currentPermissions=existingPermissions,
            )
            parent["permissions"] = permissions
            return parent

    def parsePermissionsCollection(self, newPermissionsNames, currentPermissions):
        permissionNames = list(map(lambda item: item["name"], newPermissionsNames))
        return self.checkPermissionsExistence(permissionNames, currentPermissions)

    def parsePermissionsAggregation(self, permissionTrees, currentPermissions):
        aggregatedPermissions = []
        for tree in permissionTrees:
            children = tree["children"]
            aggregatedPermissions += map(lambda c: c["name"], children)

        permissionNames = list(set(aggregatedPermissions))
        return self.checkPermissionsExistence(permissionNames, currentPermissions)

    def isPermissionMatchingPattern(self, permissionName, matchingPattern):
        if permissionName == matchingPattern:
            return True

        aTerms = permissionName.split(":")
        bTerms = matchingPattern.split(":")
        if len(aTerms) != 4 or len(bTerms) != 4:
            return False

        for i in range(4):
            if bTerms[i] == "*" or bTerms[i] == aTerms[i]:
                continue
            else:
                return False

        return True

    def checkPermissionsExistence(self, permissionNames, currentPermissions) -> List[dict]:
        """Filter the permission names from the current permissions, regex is used for filtering them
        Args:
            permissionNames (List[str]): List of permission names
            currentPermissions (List[dict]): List of permission dictionaries like the example given in 'Returns'
        Returns:
            List[dict]: Returns a list of dictionary for permissions, e.g.
            {"id": 1234, "name": api:read:identity:get_role, "allowed_actions": ["read"], "denied_actions": []}
        """
        results = []
        for name in permissionNames:
            permissionsFound = list(
                filter(
                    lambda p: self.isPermissionMatchingPattern(p["name"], name),
                    currentPermissions,
                )
            )
            for permissionFound in permissionsFound:
                results.append(permissionFound)
        return results

    # endregion Permission Tree

    # region Role
    def parseRoleTree(self, roleTree):
        roleId = self._cafmClient.ensureRoleExistence(
            name=roleTree["name"],
            title=roleTree["title"],
        )
        roleTree["id"] = roleId

        # Role permissions
        if "permissions" in roleTree:
            permissionsTrees = roleTree["permissions"]
            for permissionsTree in permissionsTrees:
                permissions = permissionsTree["permissions"]
                if "children" in permissionsTree:
                    for item in permissionsTree["children"]:
                        click.echo(click.style(f"[cafm-api] Bulk assignment of permission: {item['name']} to role name: {roleTree['name']} , role id: {roleId}"))
                else:
                    click.echo(click.style(f"[cafm-api] Bulk assignment of permissions to role id {roleId}"))
                self._bulkAssignmentPermissionsToRole(roleId=roleId, permissions=permissions)
                # for permission in permissions:
                #     permissionId = permission["id"]
                #     self._cafmClient.createAssignmentRoleToPermission(
                #         roleId,
                #         permissionId=permissionId,
                #         ignoreExistence=True,
                #     )

        # Role access
        if "access" in roleTree:
            accessibleResourceTrees = roleTree["access"]
            for resourceTree in accessibleResourceTrees:
                resourceId = resourceTree["id"]
                self._cafmClient.createAccessRoleToResource(roleId=roleId, resourceId=resourceId, ignoreExistence=True)

    def _bulkAssignmentPermissionsToRole(self, permissions, roleId):
        bulkData = []
        redisClient = Cache.instance().client()
        for permission in permissions:
            permissionId = permission["id"]
            if (
                redisClient is not None
                and redisClient.get(
                    f"{Cache.CACHE_PREFIX}assign_role_to_permission:role_id__{roleId}__permission_id__{permissionId}"
                )
                is None
            ) or (redisClient is None):
                bulkData.append(
                    dict(assign_role_to_permission=dict(data=dict(role_id=roleId, permission_id=permissionId)))
                )
        if len(bulkData) > 0:
            try:
                self._cafmClient.bulkRequest(body=dict(data=bulkData))
                # Add to cache
                for bulkDataItem in bulkData:
                    if "assign_role_to_permission" in bulkDataItem:
                        roleId = bulkDataItem["assign_role_to_permission"]["data"]["role_id"]
                        permissionId = bulkDataItem["assign_role_to_permission"]["data"]["permission_id"]
                        if redisClient is not None:
                            redisClient.setex(
                                f"{Cache.CACHE_PREFIX}assign_role_to_permission:role_id__{roleId}__permission_id__{permissionId}",
                                Cache.CACHE_TTL,
                                1,
                            )
            except Exception as e:
                click.echo(click.style(f"{e}", fg="red"))

    def parseUserTree(self, userTree):
        userId = self._cafmClient.ensureUserExistence(email=userTree["email"])
        self._cafmClient.setUserPassword(userId=userId, password=userTree["password"])

        if "roles" in userTree:
            userRoleTrees = userTree["roles"]
            for roleTree in userRoleTrees:
                roleId = roleTree["id"]
                self._cafmClient.createAssignmentRoleToUser(
                    roleId=roleId,
                    userId=userId,
                    ignoreExistence=True,
                )

    # endregion Role
