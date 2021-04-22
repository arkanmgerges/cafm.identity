"""
@author: Mohammad M. Mohammad<mmdii@develoop.run>
"""
import sys
from typing import List

sys.path.append("../../../")

import os
from dotenv import load_dotenv

import yaml
import click
import requests
from time import sleep

load_dotenv()

baseURL = os.getenv("API_URL")


@click.group()
def cli():
    pass


@cli.command(help="Create permission with permission contexts for the api endpoints")
def create_permission_with_permission_contexts_for_api_endpoints():
    click.echo(
        click.style(
            f"Creating permission with permission contexts and linking them", fg="green"
        )
    )
    token = getAccessToken()
    # Get all app routes
    appRoutesJsonResponse = appRouteList()
    # Get all the permission contexts
    permissionContextList = permissionContexts(token)
    # Get all permissions
    permissionList = permissions(token)

    apiPermissionContexts = list(
        filter(lambda x: "api_resource_type" in x["type"], permissionContextList)
    )
    apiPermissionWithContexts = apiPermissionWithContextList(
        apiPermissionContexts, appRoutesJsonResponse, permissionList
    )
    hashedKeys = hashKeys(extractKeys(apiPermissionWithContexts))
    persistPermissionWithPermissionContexts(
        apiPermissionWithContexts=apiPermissionWithContexts,
        hashedKeys=hashedKeys,
        token=token,
    )
    click.echo(
        click.style(
            f"Done creating permission with permission contexts and linking them",
            fg="green",
        )
    )
    # Logout
    click.echo(click.style(f"Logout", fg="green"))
    requests.post(
        baseURL + "/v1/identity/auth/logout",
        headers=dict(Authorization="Bearer " + token),
        json=dict(token=token),
    )


def persistPermissionWithPermissionContexts(
    apiPermissionWithContexts, hashedKeys, token
):
    for item in apiPermissionWithContexts:
        if item["create_permission_context"]:
            hashedKey = hashedKeyByKey(
                key=item["permission_context"]["path"], hashedKeys=hashedKeys
            )
            if hashedKey is not None:
                try:
                    # Persist permission context
                    data = item["permission_context"]
                    data["hash_code"] = hashedKey
                    dataItem = {"type": "api_resource_type", "data": data}
                    permContextId = persistPermissionContext(data=dataItem, token=token)

                    # Persist permission
                    permissionsDataItem = item["permissions"]
                    for permissionDataItem in permissionsDataItem:
                        permId = persistPermission(data=permissionDataItem, token=token)
                        # Link permission to permission context
                        assignPermissionToPermissionContext(
                            permissionId=permId,
                            permissionContextId=permContextId,
                            token=token,
                        )
                except Exception as e:
                    click.echo(click.style(f"{e}", fg="red"))


def assignPermissionToPermissionContext(permissionId, permissionContextId, token):
    click.echo(
        click.style(
            f"\t---> assign permission ({permissionId}) to permission context ({permissionContextId})",
            fg="yellow",
        )
    )
    resp = requests.post(
        baseURL + "/v1/identity/assignments/permission_to_permission_context",
        headers=dict(Authorization="Bearer " + token),
        json=dict(
            {
                "permission_id": permissionId,
                "permission_context_id": permissionContextId,
            }
        ),
    )
    resp.raise_for_status()
    return checkForResult(
        token,
        resp.json()["request_id"],
    )


def persistPermissionContext(data, token):
    click.echo(click.style(f"\t---> persist permission context {data}", fg="yellow"))
    resp = requests.post(
        baseURL + "/v1/identity/permission_contexts",
        headers=dict(Authorization="Bearer " + token),
        json=dict(data),
    )
    resp.raise_for_status()
    return checkForResult(
        token,
        resp.json()["request_id"],
        checkForID=True,
        resultIdName="permission_context_id",
    )


def persistPermission(data, token):
    click.echo(click.style(f"\t---> persist permission {data}", fg="yellow"))
    resp = requests.post(
        baseURL + "/v1/identity/permissions",
        headers=dict(Authorization="Bearer " + token),
        json=dict(data),
    )
    resp.raise_for_status()
    return checkForResult(
        token, resp.json()["request_id"], checkForID=True, resultIdName="permission_id"
    )


def hashedKeyByKey(key, hashedKeys) -> str:
    if "hashed_keys" in hashedKeys:
        for item in hashedKeys["hashed_keys"]:
            if item["key"] == key:
                return item["hash_code"]
    return None


def extractKeys(apiPermissionWithContexts) -> List[dict]:
    keys = []
    for item in apiPermissionWithContexts:
        if item["create_permission_context"]:
            keys.append({"key": item["permission_context"]["path"]})
    return keys


def hashKeys(keys):
    resp = requests.post(
        baseURL + "/v1/util/route/hash_keys", json=dict(unhashed_keys={"keys": keys})
    )
    return resp.json()


@cli.command(help="Create user from file")
@click.argument("file_name")
def build_resource_tree_from_file(file_name):
    try:
        token = getAccessToken()
        with open(f"{file_name}", "r") as f:
            fileData = yaml.safe_load(f)

        # Parse access tree
        for realm in fileData["realms"]:
            realmName = realm["name"]
            createRealm(token, realmName, realm["type"])
            for role in realm["roles"]:
                roleId = createRole(token, role["name"], role["title"])
                for user in role["users"]:
                    userId = createUser(token, user["email"])
                    setPassword(token, userId, user["password"])
                    assignUserToRole(token, roleId, userId)
    except Exception as e:
        click.echo(click.style(f"{e}", fg="red"))


def apiPermissionWithContextList(
    apiPermissionContexts, appRoutesJsonResponse, permissionList
):
    apiPermissionWithContexts = []
    for appRoute in appRoutesJsonResponse["routes"]:
        apiPermissionContextToBeCreated = None
        apiPermissionsToBeCreated = []
        # Check for permission contexts
        found = False
        for apiPermissionContext in apiPermissionContexts:
            if appRoute["path"] == apiPermissionContext["data"]["path"]:
                apiPermissionContexts.remove(apiPermissionContext)
                found = True
                break
        if not found:
            apiPermissionContextToBeCreated = appRoute

        # Check for permissions
        for method in appRoute["methods"]:
            if method == "post":
                method = "create"
            elif method == "put" or method == "patch":
                method = "update"
            elif method == "get":
                method = "read"
            found = False
            for permission in permissionList:
                if permission["name"] == f'api:{method}:{appRoute["name"]}':
                    found = True
                    break
            if not found:
                apiPermissionsToBeCreated.append(
                    {
                        "name": f'api:{method}:{appRoute["name"]}',
                        "allowed_actions": [method.lower()],
                        "denied_actions": [],
                    }
                )

        # Remove the methods from the permission context
        if apiPermissionContextToBeCreated is not None:
            del apiPermissionContextToBeCreated["methods"]

        apiPermissionWithContexts.append(
            {
                "create_permission_context": apiPermissionContextToBeCreated
                is not None,
                "permission_context": apiPermissionContextToBeCreated,
                "permissions": apiPermissionsToBeCreated,
            }
        )
    return apiPermissionWithContexts


def appRouteList():
    appRoutesResponse = requests.get(baseURL + "/v1/util/route/app_routes")
    appRoutesJsonResponse = appRoutesResponse.json()
    return appRoutesJsonResponse


def permissionContexts(token: str) -> List[dict]:
    permissionContextsResponse = requests.get(
        baseURL + "/v1/identity/permission_contexts?result_size=10000",
        headers=dict(Authorization="Bearer " + token),
    )
    permissionContextsJsonResponse = permissionContextsResponse.json()
    return permissionContextsJsonResponse["permission_contexts"]


def permissions(token: str) -> List[dict]:
    permissionsResponse = requests.get(
        baseURL + "/v1/identity/permissions?result_size=10000",
        headers=dict(Authorization="Bearer " + token),
    )
    permissionsJsonResponse = permissionsResponse.json()
    return permissionsJsonResponse["permissions"]


def getAccessToken():
    click.echo(click.style(f"Get Access Token", fg="green"))
    resp = requests.post(
        baseURL + "/v1/identity/auth/authenticate",
        json=dict(
            email=os.getenv("ADMIN_EMAIL", None),
            password=os.getenv("ADMIN_PASSWORD", None),
        ),
    )
    resp.raise_for_status()
    return resp.text.replace('"', "")


def createRealm(token, name, type):
    click.echo(click.style(f"Creating realm name: {name} type: {type}", fg="green"))
    resp = requests.post(
        baseURL + "/v1/identity/realms/create",
        headers=dict(Authorization="Bearer " + token),
        json=dict(name=name, realm_type=type),
    )
    resp.raise_for_status()
    checkForResult(token, resp.json()["request_id"])


def createRole(token, name, title):
    click.echo(click.style(f"Creating Role name: {name}", fg="green"))
    resp = requests.post(
        baseURL + "/v1/identity/roles/create",
        headers=dict(Authorization="Bearer " + token),
        json=dict(name=name, title=title),
    )
    resp.raise_for_status()
    return checkForResult(token, resp.json()["request_id"], checkForID=True)


def createUser(token, email):
    click.echo(click.style(f"Creating User email: {email}", fg="green"))
    resp = requests.post(
        baseURL + "/v1/identity/users/create",
        headers=dict(Authorization="Bearer " + token),
        json=dict(email=email),
    )
    resp.raise_for_status()
    return checkForResult(token, resp.json()["request_id"], checkForID=True)


def setPassword(token, user_id, password):
    click.echo(click.style(f"Set password for User: {user_id}", fg="green"))
    resp = requests.put(
        baseURL + "/v1/identity/users/" + user_id + "/set_password",
        headers=dict(Authorization="Bearer " + token),
        json=dict(password=password),
    )
    resp.raise_for_status()
    checkForResult(token, resp.json()["request_id"])


def assignUserToRole(token, roleID, userID):
    click.echo(click.style(f"Assign user To role", fg="green"))
    resp = requests.post(
        baseURL + "/v1/identity/assignments/role_to_user",
        headers=dict(Authorization="Bearer " + token),
        json=dict(role_id=roleID, user_id=userID),
    )
    resp.raise_for_status()
    checkForResult(token, resp.json()["request_id"])


def checkForResult(token, requestId, checkForID=False, resultIdName=None):
    for i in range(50):
        sleep(0.3)
        isSuccessful = requests.get(
            baseURL + "/v1/common/request/is_successful",
            headers=dict(Authorization="Bearer " + token),
            params=dict(request_id=str(requestId)),
        )
        if isSuccessful.status_code == 200:
            resp = requests.get(
                baseURL + "/v1/common/request/result",
                headers=dict(Authorization="Bearer " + token),
                params=dict(request_id=str(requestId)),
            )
            resp.raise_for_status()
            result = resp.json()["result"]
            if isSuccessful.json()["success"]:
                if checkForID:
                    if "items" in result:
                        return result["items"][0][resultIdName]
                    else:
                        return result[resultIdName]
                else:
                    return
            else:
                if "items" in result:
                    for item in result["items"]:
                        if "reason" in item:
                            raise Exception(item["reason"]["message"])
                else:
                    if "reason" in result:
                        raise Exception(result["reason"]["message"])
                raise Exception("Unknown error!")

    raise Exception("Response time out!")


if __name__ == "__main__":
    cli()
