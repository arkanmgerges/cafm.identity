import click
import requests

from time import sleep

from src.domain_model.resource.exception.CodeExceptionConstant import (
    CodeExceptionConstant,
)


class CAFMClient:
    def __init__(self, config):
        self._email = config["email"]
        self._password = config["password"]
        self._baseUrl = config["base_url"]
        self.token = None
        self.cache = None

    def getAccessToken(self, refresh=False):
        if self.token is not None and refresh is not True:
            return self.token

        resp = requests.post(
            self._baseUrl + "/v1/identity/auth/authenticate",
            json=dict(email=self._email, password=self._password),
        )
        resp.raise_for_status()
        self.token = resp.text.replace('"', "")
        click.echo(click.style(f"[cafm-api] Token retrieved {self.token}", fg="green"))

        return self.token

    def checkForResults(
        self,
        requestId,
        checkForId=False,
        resultIdName=None,
        ignoreIfExists=False,
    ):
        for i in range(50):
            click.echo(
                click.style(f"[cafm-api] {requestId}: [{i}/50] waiting ...", fg="green")
            )
            sleep(1)
            isSuccessful = requests.get(
                self._baseUrl + "/v1/common/request/is_successful",
                headers=dict(Authorization="Bearer " + self.getAccessToken()),
                params=dict(request_id=str(requestId)),
            )
            click.echo(
                click.style(
                    f"[cafm-api] {requestId}: [{i}/50] status={isSuccessful.status_code}",
                    fg="green",
                )
            )

            if isSuccessful.status_code == 200:
                resp = requests.get(
                    self._baseUrl + "/v1/common/request/result",
                    headers=dict(Authorization="Bearer " + self.getAccessToken()),
                    params=dict(request_id=str(requestId)),
                )
                resp.raise_for_status()
                result = resp.json()["result"]
                if isSuccessful.json()["success"]:
                    if checkForId:
                        if "items" in result:
                            for item in result["items"]:
                                if resultIdName in item:
                                    return item[resultIdName]
                            raise Exception(
                                f"Result items were found, but {resultIdName} is not included"
                            )
                        else:
                            return result[resultIdName]
                    else:
                        return
                else:
                    if "items" in result:
                        for item in result["items"]:
                            if "reason" in item:

                                raise Exception(
                                    f"[cafm-api] {requestId}: {item['reason']['message']}"
                                )
                    else:
                        if "reason" in result:
                            reason = result["reason"]

                            if "code" in reason:
                                if (
                                    int(reason["code"])
                                    == CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
                                ):
                                    if ignoreIfExists:
                                        click.echo(
                                            click.style(
                                                f"[cafm-api] {requestId}: Object Already Exist",
                                                fg="yellow",
                                            )
                                        )
                                        return
                            raise Exception(
                                f"[cafm-api] {requestId}: {result['reason']['message']}"
                            )
                    raise Exception("Unknown error!")
        raise Exception("Response time out!")

    # realms region

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
                raise Exception(
                    f"Multiple realms founds for name:{name} and type:{realmType}"
                )
        return None

    def createRealm(self, name, realmType):
        resp = requests.post(
            self._baseUrl + "/v1/identity/realms",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(name=name, realm_type=realmType),
        )
        resp.raise_for_status()

        realmId = self.checkForResults(
            requestId=resp.json()["request_id"],
            checkForId=True,
            resultIdName="realm_id",
        )
        click.echo(click.style(f"[cafm-api] Created realm {name}:{realmId}"))
        return realmId

    def ensureRealmExistence(self, name, realmType):
        """Reads or create realm with name and type
        Args:
            name (str): realm name
            type (str): realm type corresponding to the realm_type
        Returns resource id of realm resource
        """
        realm = self.findRealmByNameAndType(name, realmType)
        if realm is not None:
            realmId = realm["id"]
            click.echo(click.style(f"[cafm-api] Found realm {realmId}"))
            return realmId

        return self.createRealm(name, realmType)

    # end realms region

    # ou region

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
            requestId=resp.json()["request_id"],
            checkForId=True,
            resultIdName="ou_id",
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

    # end ou region

    # project region

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
            resp.json()["request_id"],
            checkForId=True,
            resultIdName="project_id",
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

    # end project region

    # assignments region

    def createAssignmentResourceToResource(self, fromId, toId, ignoreExistence=False):
        resp = requests.post(
            self._baseUrl + "/v1/identity/assignments/resource_to_resource",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(src_resource_id=fromId, dst_resource_id=toId),
        )
        resp.raise_for_status()

        self.checkForResults(
            requestId=resp.json()["request_id"],
            ignoreIfExists=ignoreExistence,
        )
        click.echo(
            click.style(f"[cafm-api] Assignment resource: {fromId} to resource: {toId}")
        )

    def createAssignmentRoleToPermission(
        self, roleId, permissionId, ignoreExistence=False
    ):
        resp = requests.post(
            self._baseUrl + "/v1/identity/assignments/role_to_permission",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(role_id=roleId, permission_id=permissionId),
        )
        resp.raise_for_status()

        self.checkForResults(
            requestId=resp.json()["request_id"],
            ignoreIfExists=ignoreExistence,
        )
        click.echo(
            click.style(
                f"[cafm-api] Assignment role: {roleId} to permission: {permissionId}"
            )
        )

    def createAccessRoleToResource(self, roleId, resourceId, ignoreExistence=False):
        resp = requests.post(
            self._baseUrl + "/v1/identity/accesses/role_to_resource",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(role_id=roleId, resource_id=resourceId),
        )
        resp.raise_for_status()

        self.checkForResults(
            requestId=resp.json()["request_id"],
            ignoreIfExists=ignoreExistence,
        )

        click.echo(
            click.style(
                f"[cafm-api] Access from role: {roleId} to resource: {resourceId}"
            )
        )

    def createAssignmentRoleToUser(self, roleId, userId, ignoreExistence=False):
        resp = requests.post(
            self._baseUrl + "/v1/identity/assignments/role_to_user",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(role_id=roleId, user_id=userId),
        )
        resp.raise_for_status()

        self.checkForResults(
            requestId=resp.json()["request_id"],
            ignoreIfExists=ignoreExistence,
        )
        click.echo(
            click.style(f"[cafm-api] Assignment role: {roleId} to user: {userId}")
        )

    # end assignments region

    # permissions region

    def readPermissions(self):
        resp = requests.get(
            self._baseUrl + "/v1/identity/permissions?result_size=10000",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
        )
        permissions = resp.json()["permissions"]
        return permissions

    # end permissions region

    # role region
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
                raise Exception(f"Multiple ous founds for name:{name}")
        return None

    def createRole(self, name, title):
        resp = requests.post(
            self._baseUrl + "/v1/identity/roles",
            headers=dict(Authorization="Bearer " + self.getAccessToken()),
            json=dict(name=name, title=title),
        )
        resp.raise_for_status()

        roleId = self.checkForResults(
            requestId=resp.json()["request_id"],
            checkForId=True,
            resultIdName="role_id",
        )
        click.echo(click.style(f"[cafm-api] Created role {name}:{roleId}"))
        return roleId

    def ensureRoleExistence(self, name, title):
        role = self.findRoleByName(name)
        if role is not None:
            roleId = role["id"]
            click.echo(click.style(f"[cafm-api] Found role {roleId}"))
            return roleId

        return self.createRole(name, title)

    # end role region

    # user region

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
            requestId=resp.json()["request_id"],
            checkForId=True,
            resultIdName="user_id",
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
            requestId=resp.json()["request_id"],
        )
        click.echo(click.style(f"[cafm-api] Updated user with password:{password}"))

    def ensureUserExistence(self, email):
        user = self.findUserByEmail(email)

        if user is not None:
            userId = user["id"]
            click.echo(click.style(f"[cafm-api] Found user {userId}"))
            return userId

        return self.createUser(email)

    # end user region