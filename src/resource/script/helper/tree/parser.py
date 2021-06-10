import click


class TreeParser:
    def __init__(self, cafmClient):
        self.cafmClient = cafmClient

    # region resource tree
    def parseResourceTree(self, parent):
        """Parses the tree nodes and creates resources by node type
        Args:
            resourceTree (obj): The parent node containing 'resource_type', 'resource_name', 'children' and other fields
        """

        if parent is None:
            return

        resource = self.ensureResourceExistence(parent)
        if resource is None:
            raise Exception(
                f"Something went wrong while ensuring resource existence for node {parent}"
            )

        for child in parent["children"]:
            childResource = self.parseResourceTree(child)
            if childResource is not None:
                self.ensureAssignmentFromParentResourceToChildResourceExistence(
                    parent=resource, child=childResource
                )

        return resource

    def ensureAssignmentFromParentResourceToChildResourceExistence(self, parent, child):
        self.cafmClient.createAssignmentResourceToResource(
            fromId=parent["id"], toId=child["id"], ignoreExistence=True
        )

    def ensureResourceExistence(self, node):
        """Create or update the resource according to the node type
        Args:
            node (obj): The node containing 'type', 'name' / 'email', 'realm_type', 'title'
        Returns an object containing the resource id of the node
        """

        if node["resource_type"] == "realm":
            resourceId = self.cafmClient.ensureRealmExistence(
                name=node["name"], realmType=node["realm_type"]
            )
            node["id"] = resourceId
            return node
        if node["resource_type"] == "ou":
            resourceId = self.cafmClient.ensureOuExistence(name=node["name"])
            node["id"] = resourceId
            return node
        if node["resource_type"] == "project":
            resourceId = self.cafmClient.ensureProjectExistence(name=node["name"])
            node["id"] = resourceId
            return node

    # end resource tree region

    # region permission tree
    def parsePermissionTree(self, parent):
        if parent["tree_type"] == "collection":
            permissions = self.parsePermissionsCollection(parent["children"])
            parent["permissions"] = permissions
            return parent

        if parent["tree_type"] == "aggregation":
            permissions = self.parsePermissionsAggregation(parent["children"])
            parent["permissions"] = permissions
            return parent

    def parsePermissionsCollection(self, permissions):
        permissionNames = list(map(lambda item: item["name"], permissions))
        return self.checkPermissionsExistence(permissionNames)

    def parsePermissionsAggregation(self, permissionTrees):
        aggregatedPermissions = []
        for tree in permissionTrees:
            children = tree["children"]
            aggregatedPermissions += map(lambda c: c["name"], children)

        permissionNames = list(set(aggregatedPermissions))
        return self.checkPermissionsExistence(permissionNames)

    def checkPermissionsExistence(self, permissionNames):
        permissions = self.cafmClient.readPermissions()

        results = []
        for name in permissionNames:
            permissionsFound = list(filter(lambda p: p["name"] == name, permissions))
            if len(permissionsFound) != 1:
                raise Exception(
                    f"{len(permissionsFound)} permissions found for name {name}"
                )
            else:
                results.append(permissionsFound[0])
        return results

    # end permission tree region

    def parseRoleTree(self, roleTree):
        roleId = self.cafmClient.ensureRoleExistence(
            name=roleTree["name"],
            title=roleTree["title"],
        )
        roleTree["id"] = roleId

        # Role permissions
        if "permissions" in roleTree:
            permissionsTrees = roleTree["permissions"]
            for permissionsTree in permissionsTrees:
                permissions = permissionsTree["permissions"]
                for permission in permissions:
                    permissionId = permission["id"]
                    self.cafmClient.createAssignmentRoleToPermission(
                        roleId,
                        permissionId=permissionId,
                        ignoreExistence=True,
                    )

        # Role access
        if "access" in roleTree:
            accessableResourceTrees = roleTree["access"]
            for resourceTree in accessableResourceTrees:
                resourceId = resourceTree["id"]
                self.cafmClient.createAccessRoleToResource(
                    roleId=roleId, resourceId=resourceId, ignoreExistence=True
                )

    def parseUserTree(self, userTree):
        userId = self.cafmClient.ensureUserExistence(email=userTree["email"])
        self.cafmClient.setUserPassword(userId=userId, password=userTree["password"])

        if "roles" in userTree:
            userRoleTrees = userTree["roles"]
            for roleTree in userRoleTrees:
                roleId = roleTree["id"]
                self.cafmClient.createAssignmentRoleToUser(
                    roleId=roleId,
                    userId=userId,
                    ignoreExistence=True,
                )