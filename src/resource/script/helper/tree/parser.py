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
        existingPermissions = self.cafmClient.readPermissions()
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
            print(f"### {permissionName} : {matchingPattern}")
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

        print(f"### {permissionName} : {matchingPattern}")
        return True

    def checkPermissionsExistence(self, permissionNames, currentPermissions):
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