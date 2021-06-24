import re
from time import sleep
from typing import List, Optional

import click
import requests

from src.domain_model.resource.exception.CodeExceptionConstant import (
    CodeExceptionConstant,
)
from src.resource.script.helper.cache.Cache import Cache
from src.resource.script.helper.cafm_api.CafmClientConfig import CafmClientConfig
from src.resource.script.helper.cafm_api.RequestCheckData import RequestCheckData


class CafmClient:
    microserviceNamePatternCompiled = re.compile("/v[0-9]/([^/]+)?/")

    def __init__(self, config: CafmClientConfig = None):
        if config is None:
            raise Exception("Cafm client config must not be none")
        self._email = config.email
        self._password = config.password
        self._baseUrl = config.baseUrl
        self._token = config.token
        self._cache = config.cache

    # region Realm

    def readRealms(self):
        resp = requests.get(
            self._baseUrl + "/v1/identity/realms?result_size=10000",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
        )
        realms = resp.json()["realms"]
        return realms

    def findRealmByNameAndType(self, name, realmType):
        realms = self.readRealms()

        realmsFound = list(
            filter(
                lambda r: (r["name"] == name and r["realm_type"] == realmType),
                realms,
            )
        )

        if len(realmsFound) > 0:
            if len(realmsFound) == 1:
                return realmsFound[0]
            else:
                raise Exception(f"Multiple realms founds for name:{name} and type:{realmType}")
        return None

    def createRealm(self, name, realmType):
        resp = requests.post(
            self._baseUrl + "/v1/identity/realms",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(name=name, realm_type=realmType),
        )
        resp.raise_for_status()

        realmId = self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
                checkForId=True,
                resultIdName="realm_id",
            )
        )
        click.echo(click.style(f"[cafm-api] Created realm {name}:{realmId}"))
        return realmId

    def ensureRealmExistence(self, name, realmType):
        """Reads or create realm with name and type
        Args:
            name (str): realm name
            realmType (str): realm type corresponding to the realm_type
        Returns resource id of realm resource
        """
        realm = self.findRealmByNameAndType(name, realmType)
        if realm is not None:
            realmId = realm["id"]
            click.echo(click.style(f"[cafm-api] Found realm {realmId}"))
            return realmId

        return self.createRealm(name, realmType)

    # endregion Realm

    # region Ou
    def readOus(self):
        resp = requests.get(
            self._baseUrl + "/v1/identity/ous?result_size=10000",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
        )
        ous = resp.json()["ous"]
        return ous

    def findOuByName(self, name):
        ous = self.readOus()

        ousFound = list(filter(lambda ou: ou["name"] == name, ous))

        if len(ousFound) > 0:
            if len(ousFound) == 1:
                return ousFound[0]
            else:
                raise Exception(f"Multiple ous founds for name:{name}")
        return None

    def createOu(self, name):
        resp = requests.post(
            self._baseUrl + "/v1/identity/ous",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(name=name),
        )
        resp.raise_for_status()

        ouId = self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
                checkForId=True,
                resultIdName="ou_id",
            )
        )
        click.echo(click.style(f"[cafm-api] Created ou {name}:{ouId}"))
        return ouId

    def ensureOuExistence(self, name):
        """Reads or create ou with name
        Args:
            name (str): realm name
        Returns resource id of ou resource
        """
        ou = self.findOuByName(name)

        if ou is not None:
            ouId = ou["id"]
            click.echo(click.style(f"[cafm-api] Found ou {ouId}"))
            return ouId

        return self.createOu(name)

    # endregion Ou

    # region Project
    def readProjects(self):
        resp = requests.get(
            self._baseUrl + "/v1/identity/projects?result_size=10000",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
        )
        projects = resp.json()["projects"]
        return projects

    def findProjectByName(self, name):
        projects = self.readProjects()

        projectsFound = list(filter(lambda p: p["name"] == name, projects))

        if len(projectsFound) > 0:
            if len(projectsFound) == 1:

                return projectsFound[0]
            else:
                raise Exception(f"Multiple projects founds for name:{name}")
        return None

    def createProject(self, name):
        resp = requests.post(
            self._baseUrl + "/v1/identity/projects",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(name=name),
        )
        resp.raise_for_status()

        projectId = self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
                checkForId=True,
                resultIdName="project_id",
            )
        )
        click.echo(click.style(f"[cafm-api] Created project {name}:{projectId}"))
        return projectId

    def ensureProjectExistence(self, name):
        project = self.findProjectByName(name)

        if project is not None:
            projectId = project["id"]
            click.echo(click.style(f"[cafm-api] Found project {projectId}"))
            return projectId

        return self.createProject(name)

    # endregion Project

    # region Assignment

    def createAssignmentResourceToResource(self, fromId, toId, ignoreExistence=False):
        resp = requests.post(
            self._baseUrl + "/v1/identity/assignments/resource_to_resource",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(src_resource_id=fromId, dst_resource_id=toId),
        )
        resp.raise_for_status()

        self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
                ignoreIfExists=ignoreExistence,
            )
        )
        click.echo(click.style(f"[cafm-api] Assignment resource: {fromId} to resource: {toId}"))

    def createAssignmentRoleToPermission(self, roleId, permissionId, ignoreExistence=False):
        resp = requests.post(
            self._baseUrl + "/v1/identity/assignments/role_to_permission",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(role_id=roleId, permission_id=permissionId),
        )
        resp.raise_for_status()

        self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
                ignoreIfExists=ignoreExistence,
            )
        )
        click.echo(click.style(f"[cafm-api] Assignment role: {roleId} to permission: {permissionId}"))

    def createAccessRoleToResource(self, roleId, resourceId, ignoreExistence=False):
        resp = requests.post(
            self._baseUrl + "/v1/identity/accesses/role_to_resource",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(role_id=roleId, resource_id=resourceId),
        )
        resp.raise_for_status()

        self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
                ignoreIfExists=ignoreExistence,
            )
        )

        click.echo(click.style(f"[cafm-api] Access from role: {roleId} to resource: {resourceId}"))

    def createAssignmentRoleToUser(self, roleId, userId, ignoreExistence=False):
        resp = requests.post(
            self._baseUrl + "/v1/identity/assignments/role_to_user",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(role_id=roleId, user_id=userId),
        )
        resp.raise_for_status()

        self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
                ignoreIfExists=ignoreExistence,
            )
        )
        click.echo(click.style(f"[cafm-api] Assignment role: {roleId} to user: {userId}"))

    # endregion Assignment

    # region Permission

    def readPermissions(self):
        resp = requests.get(
            self._baseUrl + "/v1/identity/permissions?result_size=10000",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
        )
        permissions = resp.json()["permissions"]
        return permissions

    def permissions(self) -> List[dict]:
        permissionsResponse = requests.get(
            self._baseUrl + "/v1/identity/permissions?result_size=10000",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
        )
        permissionsJsonResponse = permissionsResponse.json()
        return permissionsJsonResponse["permissions"]

    def permissionContexts(self) -> List[dict]:
        permissionContextsResponse = requests.get(
            self._baseUrl + "/v1/identity/permission_contexts?result_size=10000",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
        )
        permissionContextsJsonResponse = permissionContextsResponse.json()
        return permissionContextsJsonResponse["permission_contexts"]

    def creatPermissionWithPermissionContextsForApiEndpoints(self):
        # Get all app routes
        appRoutesJsonResponse = self.appRouteList()
        # Get all the permission contexts
        permissionContextList = self.permissionContexts()

        apiPermissionContexts = list(filter(lambda x: "api_resource_type" in x["type"], permissionContextList))

        apiPermissionWithContexts = self._apiPermissionWithContextList(
            apiPermissionContexts, appRoutesJsonResponse
        )
        hashedKeys = self.hashKeys(self._extractKeys(apiPermissionWithContexts))
        self._bulkPersistPermissionWithPermissionContexts(
            apiPermissionWithContexts=apiPermissionWithContexts,
            hashedKeys=hashedKeys,
        )

    def _apiPermissionWithContextList(self, apiPermissionContexts, appRoutesJsonResponse):
        apiPermissionWithContexts = []
        for appRoute in appRoutesJsonResponse["routes"]:
            apiPermissionContextToBeCreated = None
            apiPermissionsToBeCreated = []
            # Check for permission contexts
            apiPermissionContextFound = False
            for apiPermissionContext in apiPermissionContexts:
                if appRoute["path"] == apiPermissionContext["data"]["path"]:
                    apiPermissionContextFound = True
                    apiPermissionContexts.remove(apiPermissionContext)
                    apiPermissionContextToBeCreated = {"name": appRoute["path"], "path": appRoute["path"]}
                    break
            if not apiPermissionContextFound:
                apiPermissionContextToBeCreated = {"name": appRoute["path"], "path": appRoute["path"]}

            # Check for permissions
            for method in appRoute["methods"]:
                if method == "post":
                    method = "create"
                elif method == "put" or method == "patch":
                    method = "update"
                elif method == "get":
                    method = "read"

                microserviceName = self._extractMicroserviceName(appRoute["path"])
                apiPermissionsToBeCreated.append(
                    {
                        "name": f'api:{method}:{microserviceName}:{appRoute["name"]}',
                        "allowed_actions": [method.lower()],
                        "denied_actions": [],
                    }
                )

            apiPermissionWithContexts.append(
                {
                    "permission_context": apiPermissionContextToBeCreated,
                    "permissions": apiPermissionsToBeCreated,
                }
            )
        return apiPermissionWithContexts

    def _extractMicroserviceName(self, routePath):
        m = CafmClient.microserviceNamePatternCompiled.search(routePath)
        if m.group(1):
            return m.group(1)
        else:
            return None

    def _bulkPersistPermissionWithPermissionContexts(self, apiPermissionWithContexts, hashedKeys):
        bulkData = []
        redisClient = None
        try:
            redisClient = Cache.instance().client()
        except:
            pass

        for item in apiPermissionWithContexts:
            hashedKey = self._hashedKeyByKey(key=item["permission_context"]["path"], hashedKeys=hashedKeys)
            if hashedKey is not None:
                permissionsDataItem = item["permissions"]
                addPermissionContext = False
                for permissionDataItem in permissionsDataItem:
                    if (
                        redisClient is not None
                        and redisClient.get(f'{Cache.CACHE_PREFIX}permission_name:{permissionDataItem["name"]}') is None
                    ) or (redisClient is None):
                        bulkData.append(dict(create_permission=dict(data=permissionDataItem)))
                        addPermissionContext = True
                if addPermissionContext:
                    data = item["permission_context"]
                    data["hash_code"] = hashedKey
                    bulkData.append(
                        dict(create_permission_context=dict(data=dict(type="api_resource_type", data=data)))
                    )

        try:
            if len(bulkData) > 0:
                bulkResponse = self.bulkRequest(body=dict(data=bulkData), returnResponse=True)
                # Link permission to permission context
                bulkMapData = self._mapPermissionToPermissionContextByBulkResponse(
                    apiPermissionWithContexts=apiPermissionWithContexts, bulkResponse=bulkResponse
                )
                if len(bulkMapData) > 0:
                    self.bulkRequest(body=dict(data=bulkMapData))

                # Add to cache
                for bulkDataItem in bulkData:
                    if "create_permission" in bulkDataItem:
                        permissionName = bulkDataItem["create_permission"]["data"]["name"]
                        if redisClient is not None:
                            redisClient.setex(
                                f"{Cache.CACHE_PREFIX}permission_name:{permissionName}", Cache.CACHE_TTL, 1
                            )

        except Exception as e:
            click.echo(click.style(f"{e}", fg="red"))

    def _mapPermissionToPermissionContextByBulkResponse(self, apiPermissionWithContexts, bulkResponse):
        permissionToPermissionContextMap = []
        for item in apiPermissionWithContexts:
            # It will search the data from the response, and if the response does not have what we are searching for,
            # then no assignments will happen
            permissionContextId = self._findIdByNameInResponse(
                name=item["permission_context"]["name"], bulkResponse=bulkResponse
            )
            if permissionContextId is not None:
                for permission in item["permissions"]:
                    permissionId = self._findIdByNameInResponse(name=permission["name"], bulkResponse=bulkResponse)
                    if permissionId is not None:
                        permissionToPermissionContextMap.append(
                            dict(
                                assign_permission_to_permission_context=dict(
                                    data=dict(
                                        permission_id=permissionId,
                                        permission_context_id=permissionContextId,
                                    )
                                )
                            )
                        )

        return permissionToPermissionContextMap

    def _extractKeys(self, apiPermissionWithContexts) -> List[dict]:
        keys = []
        for item in apiPermissionWithContexts:
            if (item is not None and "permission_context" in item) and (item["permission_context"] is not None and "path" in item["permission_context"]):
                keys.append({"key": item["permission_context"]["path"]})
        return keys

    def _hashedKeyByKey(self, key, hashedKeys) -> Optional[str]:
        if "hashed_keys" in hashedKeys:
            for item in hashedKeys["hashed_keys"]:
                if item["key"] == key:
                    return item["hash_code"]
        return None

    def _findIdByNameInResponse(self, name, bulkResponse):
        for item in bulkResponse["items"]:
            data = item["data"]
            if data["command"] == "create_permission_context":
                data = data["command_data"]
                if data["data"]["name"] == name:
                    return data["permission_context_id"]
            elif data["command"] == "create_permission":
                data = data["command_data"]
                if data["name"] == name:
                    return data["permission_id"]
        return None

    # endregion Permission

    # region Role
    def readRoles(self):
        resp = requests.get(
            self._baseUrl + "/v1/identity/roles?result_size=10000",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
        )
        roles = resp.json()["roles"]
        return roles

    def findRoleByName(self, name):
        roles = self.readRoles()
        rolesFound = list(filter(lambda r: r["name"] == name, roles))
        if len(rolesFound) > 0:
            if len(rolesFound) == 1:

                return rolesFound[0]
            else:
                raise Exception(f"Multiple roles founds for name:{name}")
        return None

    def createRole(self, name, title):
        resp = requests.post(
            self._baseUrl + "/v1/identity/roles",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(name=name, title=title),
        )
        resp.raise_for_status()

        roleId = self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
                checkForId=True,
                resultIdName="role_id",
            )
        )
        click.echo(click.style(f"[cafm-api] Created role {name}:{roleId}"))
        return roleId

    def assignTagToRole(self, tagName, roleId):
        resp = requests.post(
            self._baseUrl + "/v1/project/tags/assign_tag_to_role",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(name=tagName, role_id=roleId),
        )
        # resp.raise_for_status()

        click.echo(click.style(f"[cafm-api] Assign tag to role {tagName}:{roleId}"))
        return None

    def ensureRoleExistence(self, name, title):
        role = self.findRoleByName(name)
        if role is not None:
            roleId = role["id"]
            click.echo(click.style(f"[cafm-api] Found role {roleId}"))
            return roleId

        return self.createRole(name, title)

    # endregion Role

    # region User

    def readUsers(self):
        resp = requests.get(
            self._baseUrl + "/v1/identity/users?result_size=10000",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
        )
        users = resp.json()["users"]
        return users

    def findUserByEmail(self, email):
        users = self.readUsers()
        usersFound = list(filter(lambda u: u["email"] == email, users))
        if len(usersFound) > 0:
            if len(usersFound) == 1:
                return usersFound[0]
            else:
                raise Exception(f"Multiple users founds for email:{email}")
        return None

    def createUser(self, email):
        resp = requests.post(
            self._baseUrl + "/v1/identity/users",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(email=email),
        )
        resp.raise_for_status()

        userId = self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
                checkForId=True,
                resultIdName="user_id",
            )
        )
        click.echo(click.style(f"[cafm-api] Created user {email}:{userId}"))
        return userId

    def setUserPassword(self, userId, password):
        resp = requests.put(
            self._baseUrl + f"/v1/identity/users/{userId}/set_password",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(password=password),
        )
        resp.raise_for_status()

        self.checkForResults(
            RequestCheckData(
                requestId=resp.json()["request_id"],
            )
        )
        click.echo(click.style(f"[cafm-api] Updated user with password:{password}"))

    def ensureUserExistence(self, email):
        user = self.findUserByEmail(email)

        if user is not None:
            userId = user["id"]
            click.echo(click.style(f"[cafm-api] Found user {userId}"))
            return userId

        return self.createUser(email)

    # endregion User

    # region Route
    def appRouteList(self):
        appRoutesResponse = requests.get(self._baseUrl + "/v1/util/route/app_routes")
        appRoutesJsonResponse = appRoutesResponse.json()
        return appRoutesJsonResponse

    # endregion

    # region Misc
    def hashKeys(self, keys):
        resp = requests.post(self._baseUrl + "/v1/util/route/hash_keys", json=dict(unhashed_keys={"keys": keys}))
        return resp.json()

    def getAccessToken(self, refresh=False):
        if self._token is not None and refresh is not True:
            return self._token

        resp = requests.post(
            self._baseUrl + "/v1/identity/auth/authenticate",
            json=dict(email=self._email, password=self._password),
        )
        resp.raise_for_status()
        self._token = resp.text.replace('"', "")
        click.echo(click.style(f"[cafm-api] Token retrieved {self._token}", fg="green"))

        return self._token

    def bulkRequest(self, body, returnResponse=False):
        resp = requests.post(
            self._baseUrl + "/v1/common/_bulk",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(body=body),
        )
        resp.raise_for_status()

        requestId = resp.json()["request_id"]
        bulkResponse = self.checkForResults(
            RequestCheckData(requestId=requestId, ignoreIfExists=True, returnResult=returnResponse)
        )
        click.echo(click.style(f"[cafm-api] Bulk request with request id: {requestId}"))

        if returnResponse:
            return bulkResponse

    def checkForResults(self, requestCheckData: RequestCheckData):
        period = 0.3
        for i in range(50):
            click.echo(click.style(f"[cafm-api] {requestCheckData.requestId}: [{i}/50] waiting ...", fg="green"))
            sleep(period)
            isSuccessful = requests.get(
                self._baseUrl + "/v1/common/request/is_successful",
                headers=dict(Authorization="Bearer " + self.getAccessToken()),
                params=dict(request_id=str(requestCheckData.requestId)),
            )
            click.echo(
                click.style(
                    f"[cafm-api] {requestCheckData.requestId}: [{i}/50] status={isSuccessful.status_code}",
                    fg="green",
                )
            )

            if isSuccessful.status_code == 200:
                resp = requests.get(
                    self._baseUrl + "/v1/common/request/result",
                    headers=dict(Authorization="Bearer " + self.getAccessToken()),
                    params=dict(request_id=str(requestCheckData.requestId)),
                )
                resp.raise_for_status()
                result = resp.json()["result"]
                if isSuccessful.json()["success"]:
                    if requestCheckData.returnResult:
                        if requestCheckData.checkForId:
                            if "items" in result:
                                for item in result["items"]:
                                    if requestCheckData.resultIdName in item:
                                        return item[requestCheckData.resultIdName]
                                raise Exception(
                                    f"Result items were found, but {requestCheckData.resultIdName} is not included"
                                )
                            else:
                                return result[requestCheckData.resultIdName]
                        else:
                            return result
                    else:
                        return
                else:
                    if "items" in result:
                        for item in result["items"]:
                            if "reason" in item:

                                raise Exception(f"[cafm-api] {requestCheckData.requestId}: {item['reason']['message']}")
                    else:
                        if "reason" in result:
                            reason = result["reason"]

                            if "code" in reason:
                                if int(reason["code"]) == CodeExceptionConstant.OBJECT_ALREADY_EXIST.value:
                                    if requestCheckData.ignoreIfExists:
                                        click.echo(
                                            click.style(
                                                f"[cafm-api] {requestCheckData.requestId}: Object Already Exist",
                                                fg="yellow",
                                            )
                                        )
                                        return
                            raise Exception(f"[cafm-api] {requestCheckData.requestId}: {result['reason']['message']}")
                    raise Exception("Unknown error!")
            period += 0.2
        raise Exception("Response time out!")

    # endregion Misc
