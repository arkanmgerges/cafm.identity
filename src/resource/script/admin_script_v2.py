"""
@author: Mohammad M. Mohammad<mmdii@develoop.run>
"""
import sys
import uuid
import os
import yaml
import click
import re
import requests
import redis

from copy import copy
from pyArango.connection import Connection
from typing import List, Optional


from confluent_kafka.avro import CachedSchemaRegistryClient
from pyArango.connection import Connection
from pyArango.query import AQLQuery
from pyArango.users import Users
from confluent_kafka.admin import AdminClient, NewTopic


from src.port_adapter.messaging.common.model.IdentityCommand import IdentityCommand
from src.port_adapter.messaging.common.model.IdentityEvent import IdentityEvent

sys.path.append("../../../")

from dotenv import load_dotenv
from time import sleep

load_dotenv()

baseURL = os.getenv("API_URL")
microserviceNamePatternCompiled = re.compile("/v[0-9]/([^/]+)?/")


@click.group()
def cli():
    pass


@cli.command(help="Check that schema registry is ready")
def check_schema_registry_readiness():
    click.echo(click.style("[Schema Registry] Check readiness", fg="green"))

    config = {"url": os.getenv("MESSAGE_SCHEMA_REGISTRY_URL", "")}
    counter = 15
    seconds = 10

    while counter > 0:
        try:
            counter = counter - 1

            click.echo(click.style("[Schema Registry] Sending request ...", fg="green"))
            srClient = CachedSchemaRegistryClient(config)
            srClient.get_latest_schema(subject="test")
            click.echo(click.style("[Schema Registry] Ready", fg="green"))

            exit(0)
        except Exception as e:
            click.echo(click.style(f"[Schema Registry] Error: {e}", fg="red"))
            click.echo(click.style(f"[Schema Registry] Retry in {seconds}s"))
            click.echo(click.style(f"[Schema Registry] Remaining retries {counter}/15"))
            sleep(seconds)
            seconds += 3

    exit(1)


@cli.command(help="Check that redis is ready")
def check_redis_readiness():
    click.echo(click.style("[Redis] Check readiness", fg="green"))

    config = {
        "host": os.getenv("CAFM_IDENTITY_REDIS_HOST", "localhost"),
        "port": os.getenv("CAFM_IDENTITY_REDIS_PORT", 6379),
    }
    counter = 15
    seconds = 10

    while counter > 0:
        try:
            cache: redis.client.Redis = redis.Redis(**config)
            click.echo(click.style("[Redis] Client created", fg="green"))

            cache.setex("test_redis_key", 10, "test")
            click.echo(click.style("[Redis] Test entry added", fg="green"))

            if cache.exists("test_redis_key"):
                click.echo(click.style("[Redis] Test entry found", fg="green"))
                click.echo(click.style("[Redis] Ready", fg="green"))
                exit(0)

            click.echo(click.style(f"[Redis] Entry not found", fg="yellow"))
            click.echo(click.style(f"[Redis] Sleep {seconds}s", fg="green"))
            sleep(seconds)
            seconds += 3
        except Exception as e:
            click.echo(click.style(f"[Redis] Error: {e}", fg="red"))
            click.echo(click.style(f"[Redis] Sleep {seconds}s", fg="green"))
            sleep(seconds)
            seconds += 3

    exit(1)


@cli.command(help="Initialize Kafka topics")
def init_kafka_topics():
    click.echo(click.style("[Kafka] Init topics", fg="green"))

    config = {"bootstrap.servers": os.getenv("MESSAGE_BROKER_SERVERS", "")}
    adminClient = AdminClient(config)
    click.echo(click.style("[Kafka] Client created", fg="green"))

    installedTopics = adminClient.list_topics().topics.keys()
    requiredTopics = [
        "cafm.identity.cmd",
        "cafm.identity.evt",
        "cafm.identity.api-failed-cmd-handle",
        "cafm.identity.failed-cmd-handle",
        "cafm.identity.failed-evt-handle",
        "cafm.identity.project-failed-evt-handle",
    ]
    newTopics = [
        NewTopic(
            requiredTopic,
            num_partitions=int(os.getenv("KAFKA_PARTITIONS_COUNT_PER_TOPIC", 1)),
            replication_factor=1,
        )
        for requiredTopic in requiredTopics
        if requiredTopic not in installedTopics
    ]

    if len(newTopics) > 0:
        kafkaFuture = adminClient.create_topics(newTopics)
        for topicName, topicFuture in kafkaFuture.items():
            counter = 5
            seconds = 5
            while counter > 0:
                try:
                    counter -= 1
                    topicFuture.result()
                    click.echo(click.style(f"[Kafka] Topic {topicName} created"))
                except Exception as e:
                    click.echo(click.style(f"[Kafka] Failed to create {topicName}"))
                    click.echo(click.style(f"[Kafka] Error {e}", fg="red"))
                    click.echo(click.style(f"[Kafka] Retry in {seconds}s", fg="red"))
                    sleep(seconds)
    else:
        click.echo(click.style(f"[Kafka] All topics already exist"))


@cli.command(help="Initialize Schema Registry")
def init_schema_registry():
    click.echo(click.style("[Schema Registry] Init", fg="green"))

    config = {"url": os.getenv("MESSAGE_SCHEMA_REGISTRY_URL", "")}
    srClient = CachedSchemaRegistryClient(config)
    click.echo(click.style("[Schema Registry] Client created", fg="green"))

    requiredSchemas = [
        {"name": "cafm.identity.Command", "schema": IdentityCommand.get_schema()},
        {"name": "cafm.identity.Event", "schema": IdentityEvent.get_schema()},
    ]
    newSchemas = []

    for schema in requiredSchemas:
        s = srClient.get_latest_schema(subject=schema["name"])
        if s[0] is None:
            newSchemas.append(schema)
        else:
            click.echo(
                click.style(f'[Schema Registry] Schema {schema["name"]} already exists')
            )

    for schema in newSchemas:
        srClient.register(schema["name"], schema["schema"])
        click.echo(
            click.style(f'[Schema Registry] Schema {schema["name"]} was created')
        )

    exit(0)


@cli.command(help="Initialize Arango database")
def init_arango_db():
    click.echo(click.style("[Arango] Init database", fg="green"))

    dbName = os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", None)
    if dbName is None:
        raise Exception("Database name {CAFM_IDENTITY_ARANGODB_DB_NAME} is not set")

    try:
        conn = dbClientConnection()

        counter = 30
        seconds = 3
        while counter > 0:
            counter -= 1
            if conn.hasDatabase(dbName):
                click.echo(click.style(f"[Arango] {dbName} is available", fg="green"))
                break

            conn.createDatabase(name=dbName)
            conn.reload()
            click.echo(click.style(f"[Arango] {dbName} was created", fg="green"))
            sleep(seconds)
            seconds += 3

        db = conn[dbName]

        click.echo(click.style(f"[Arango] Creating collections ..."))
        collectionNames = [
            "resource",
            "permission",
            "permission_context",
            "country",
            "city",
        ]
        for name in collectionNames:
            if db.hasCollection(name):
                click.echo(click.style(f"[Arango] Collection {name} already exists"))
                continue

            db.createCollection(
                name=name, keyOptions={"type": "uuid", "allowUserKeys": True}
            )
            click.echo(click.style(f"[Arango] Collection {name} was created"))

        click.echo(click.style(f"[Arango] Creating edges ..."))
        edgeNames = ["has", "for", "access", "owned_by"]
        for name in edgeNames:
            if db.hasCollection(name):
                click.echo(click.style(f"[Arango] Edge {name} already exists"))
                continue

            db.createCollection(
                className="Edges",
                name=name,
                keyOptions={"type": "uuid", "allowUserKeys": True},
            )
            click.echo(click.style(f"[Arango] Edge {name} was created"))

        # click.echo(click.style(f"[Arango] Creating default permission contexts ..."))
        # permissionContextResourceNames = [
        #     "realm",
        #     "ou",
        #     "project",
        #     "user",
        #     "role",
        #     "user_group",
        # ]
        # for permissionContextResourceName in permissionContextResourceNames:
        #     aql = """
        #                 UPSERT {data: {name: @resourceTypeName}}
        #                     INSERT {_key: @id, id: @id, type: @type, data: @data}
        #                     UPDATE {data: @data}
        #                   IN permission_context
        #                 """

        #     bindVars = {
        #         "id": str(uuid.uuid4()),
        #         "type": "resource_type",
        #         "resourceTypeName": permissionContextResourceName,
        #         "data": {
        #             "name": permissionContextResourceName,
        #             "type": "resource_type",
        #         },
        #     }
        #     queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        # click.echo(
        #     click.style(
        #         f"[Arango] Creating default permissions for permission contexts ..."
        #     )
        # )
        # # Add default permissions (this was added later in code. It will read the already created permission contexts and
        # # create permissions for them)
        # # Fetch all permission contexts
        # aql = """
        #     FOR pc IN permission_context
        #         RETURN pc
        # """
        # permissionContextsQueryResult = db.AQLQuery(aql, rawResults=True)
        # permissionContextsResult = []
        # for r in permissionContextsQueryResult:
        #     permissionContextsResult.append(r)

        # # Create permissions with names '<action>_<permission_context>' like read_ou, create_realm ...etc
        # click.echo(
        #     click.style(
        #         f"[Arango] Create permissions with names linked to permission contexts"
        #     )
        # )
        # for action in ["create", "read", "update", "delete"]:
        #     for pc in permissionContextsResult:
        #         aql = """
        #                 UPSERT {name: @name, type: @type}
        #                     INSERT {_key: @id, id: @id, name: @name, type: @type, allowed_actions: ["#allowedAction"], denied_actions: []}
        #                     UPDATE {name: @name}
        #                   IN permission
        #                 """
        #         aql = aql.replace("#allowedAction", action)
        #         bindVars = {
        #             "id": str(uuid.uuid4()),
        #             "name": f'{action}_{pc["data"]["name"]}',
        #             "type": "permission",
        #         }
        #         queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        # click.echo(click.style(f"[Arango] Fetch all permissions"))
        # aql = """
        #     FOR p IN permission
        #         RETURN p
        # """
        # permissionsResult = db.AQLQuery(aql, rawResults=True)

        # click.echo(click.style(f"[Arango] Link permissions to permission contexts"))
        # for perm in permissionsResult:
        #     aql = """
        #         UPSERT {_from: @fromId, _to: @toId}
        #             INSERT {_from: @fromId, _to: @toId, _from_type: 'permission', _to_type: 'permission_context'}
        #             UPDATE {_from: @fromId, _to: @toId, _from_type: 'permission', _to_type: 'permission_context'}
        #           IN `for`
        #         """
        #     rtName = perm["name"][perm["name"].find("_") + 1 :]
        #     rtId = None
        #     for pc in permissionContextsResult:
        #         if pc["data"]["name"] == rtName:
        #             rtId = pc["_id"]
        #             break
        #     if rtId is None:
        #         click.echo(click.style(f"rtId is none for {rtName}", fg="red"))

        #     if rtId is not None:
        #         bindVars = {"fromId": perm["_id"], "toId": rtId}
        #         queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    except Exception as e:
        click.echo(click.style(f"[Arango] Something went wrong", fg="yellow"))
        click.echo(click.style(f"[Arango] Error {e}", fg="red"))
        exit(1)

    exit(0)


@cli.command(help="Create an admin user for Arango database")
@click.argument("email")
@click.argument("password")
@click.argument("database_name")
def create_arango_db_user(email, password, database_name):
    click.echo(
        click.style(
            f"[Arango] Creating an admin user with username: {email} for the database: {database_name}",
            fg="green",
        )
    )

    conn = dbClientConnection()
    users = Users(connection=conn)
    click.echo(click.style("[Arango] Current users fetched", fg="green"))

    user = None
    try:
        user = users.fetchUser(username=email)
        click.echo(click.style(f"[Arango] User {email} fetched", fg="green"))
    except Exception as e:
        click.echo(click.style(f"[Arango] No user {email} fetched", fg="yellow"))

    # Create User
    if user is None:
        try:
            user = users.createUser(email, password)
            user.save()
            click.echo(click.style(f"[Arango] User {email} created", fg="green"))

            user.setPermissions(dbName=database_name, access=True)
            click.echo(click.style(f"[Arango] Permissions set for {email}", fg="green"))
        except Exception as e:
            click.echo(click.style(f"[Arango] Error: {e}", fg="red"))
            exit(1)

    exit(0)


def dbClientConnection():
    config = {
        "arangoURL": os.getenv("CAFM_IDENTITY_ARANGODB_URL", ""),
        "username": os.getenv("CAFM_IDENTITY_ARANGODB_USERNAME", ""),
        "password": os.getenv("CAFM_IDENTITY_ARANGODB_PASSWORD", ""),
    }
    try:
        connection = Connection(**config)
        return connection
    except Exception as e:
        raise Exception(f"Could not connect to the db, message: {e}")


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


def persistPermissionWithPermissionContexts(apiPermissionWithContexts, hashedKeys):
    permissionContextDataList = []
    permissionDataList = []
    permissionToPermissionContextDataList = []
    for item in apiPermissionWithContexts:
        if item["create_permission_context"]:
            hashedKey = hashedKeyByKey(
                key=item["permission_context"]["path"], hashedKeys=hashedKeys
            )
            if hashedKey is not None:
                permissionContextId = _generateUuid3ByString(hashedKey)
                data = item["permission_context"]
                data["hash_code"] = hashedKey
                permissionContextDataList.append(
                    {
                        "_key": permissionContextId,
                        "id": permissionContextId,
                        "type": "api_resource_type",
                        "data": data,
                    }
                )

                permissionsDataItem = item["permissions"]
                for permissionDataItem in permissionsDataItem:
                    permissionId = _generateUuid3ByString(permissionDataItem["name"])
                    permissionDataItem["id"] = permissionId
                    permissionDataItem["_key"] = permissionId
                    permissionDataList.append(permissionDataItem)

                    # Link permission to permission context
                    forId = _generateUuid3ByString(
                        f"{permissionId}{permissionContextId}"
                    )
                    permissionToPermissionContextDataList.append(
                        {
                            "_key": forId,
                            "_from": f"permission/{permissionId}",
                            "_to": f"permission_context/{permissionContextId}",
                            "_from_type": "permission",
                            "_to_type": "permission_context",
                        }
                    )

    try:
        connection = _dbClientConnection()
        db = connection[os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", "cafm-identity")]
        permissionCollection = db["permission"]
        permissionContextCollection = db["permission_context"]
        forCollection = db["for"]
        forCollection.bulkSave(
            docs=permissionToPermissionContextDataList, onDuplicate="replace"
        )
        permissionContextCollection.bulkSave(
            docs=permissionContextDataList, onDuplicate="replace"
        )
        permissionCollection.bulkSave(docs=permissionDataList, onDuplicate="replace")
    except Exception as e:
        click.echo(click.style(f"{e}", fg="red"))


def _generateUuid3ByString(string) -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_URL, string))


def _dbClientConnection():
    try:
        connection = Connection(
            arangoURL=os.getenv("CAFM_IDENTITY_ARANGODB_URL", ""),
            username=os.getenv("CAFM_IDENTITY_ARANGODB_USERNAME", ""),
            password=os.getenv("CAFM_IDENTITY_ARANGODB_PASSWORD", ""),
        )
        return connection
    except Exception as e:
        raise Exception(f"Could not connect to the db, message: {e}")


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


def hashedKeyByKey(key, hashedKeys) -> Optional[str]:
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
            apiPermissionContextToBeCreated = copy(appRoute)
            apiPermissionContextToBeCreated["name"] = appRoute["path"]

        # Check for permissions
        for method in appRoute["methods"]:
            if method == "post":
                method = "create"
            elif method == "put" or method == "patch":
                method = "update"
            elif method == "get":
                method = "read"
            found = False
            microserviceName = _extractMicroserviceName(appRoute["path"])
            for permission in permissionList:
                microserviceName = (
                    microserviceName if microserviceName is not None else "default"
                )
                if (
                    permission["name"]
                    == f'api:{method}:{microserviceName}:{appRoute["name"]}'
                ):
                    found = True
                    break
            if not found:
                apiPermissionsToBeCreated.append(
                    {
                        "name": f'api:{method}:{microserviceName}:{appRoute["name"]}',
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


def _extractMicroserviceName(routePath):
    m = microserviceNamePatternCompiled.search(routePath)
    if m.group(1):
        return m.group(1)
    else:
        return None


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
