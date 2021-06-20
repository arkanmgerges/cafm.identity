"""
@author: Mohammad M. Mohammad<mmdii@develoop.run>
@collaborator: Alex Brebu<alexandru.brebu@digitalmob.ro>
@collaborator: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import inspect
import os
import sys
import uuid

import click
import redis
import yaml
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import CachedSchemaRegistryClient
from pyArango.users import Users

from src.port_adapter.messaging.common.model.IdentityCommand import IdentityCommand
from src.port_adapter.messaging.common.model.IdentityEvent import IdentityEvent
from src.resource.script.helper.arango.ArangoClient import ArangoClient
from src.resource.script.helper.cache.Cache import Cache
from src.resource.script.helper.cafm_api.CafmClient import CafmClient
from src.resource.script.helper.cafm_api.CafmClientConfig import CafmClientConfig
from src.resource.script.helper.tree.TreeParser import TreeParser

sys.path.append("../../../")

from dotenv import load_dotenv
from time import sleep

load_dotenv()

baseURL = os.getenv("API_URL")


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


@cli.command(help="Create super admin user")
def create_super_admin_user():
    cafmClient = CafmClient(
        CafmClientConfig(
            email="user@admin.system",
            password="1234",
            baseUrl=os.getenv("API_URL"),
            cache=Cache.instance()
        )
    )
    roleId = cafmClient.ensureRoleExistence("super_admin", "Super Admin")
    userId = cafmClient.ensureUserExistence(os.getenv("ADMIN_EMAIL", "admin@local.me"))
    cafmClient.setUserPassword(userId=userId, password=os.getenv("ADMIN_PASSWORD", "1234"))
    cafmClient.createAssignmentRoleToUser(roleId=roleId, userId=userId, ignoreExistence=True)


@cli.command(help="Check that redis is ready")
def check_redis_readiness():
    click.echo(click.style("[Redis] Check readiness", fg="green"))

    counter = 15
    seconds = 10

    while counter > 0:
        try:
            cache: redis.client.Redis = Cache.instance().client()
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
            click.echo(click.style(f'[Schema Registry] Schema {schema["name"]} already exists'))

    for schema in newSchemas:
        srClient.register(schema["name"], schema["schema"])
        click.echo(click.style(f'[Schema Registry] Schema {schema["name"]} was created'))

    exit(0)


@cli.command(help="Initialize Arango database")
def init_arango_db():
    click.echo(click.style("[Arango] Init database", fg="green"))

    dbName = os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", None)
    if dbName is None:
        raise Exception("Database name {CAFM_IDENTITY_ARANGODB_DB_NAME} is not set")

    try:
        arangoClient = ArangoClient.clientByDefaultEnv()
        conn = arangoClient.getConnection()

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

            db.createCollection(name=name, keyOptions={"type": "uuid", "allowUserKeys": True})
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

        click.echo(click.style(f"[Arango] Creating default permission contexts ..."))
        permissionContextResourceNames = [
            "realm",
            "ou",
            "project",
            "user",
            "role",
            "user_group",
        ]
        for permissionContextResourceName in permissionContextResourceNames:
            aql = """
                        UPSERT {data: {name: @resourceTypeName}}
                            INSERT {_key: @id, id: @id, type: @type, data: @data}
                            UPDATE {data: @data}
                          IN permission_context
                        """

            bindVars = {
                "id": str(uuid.uuid4()),
                "type": "resource_type",
                "resourceTypeName": permissionContextResourceName,
                "data": {
                    "name": permissionContextResourceName,
                    "type": "resource_type",
                },
            }
            _queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        click.echo(click.style(f"[Arango] Creating default permissions for permission contexts ..."))
        # Add default permissions (this was added later in code. It will read the already created permission contexts and
        # create permissions for them)
        # Fetch all permission contexts
        aql = """
            FOR pc IN permission_context
                FILTER 
                    pc.type == "resource_type" AND
                    (pc.data.name == "realm" OR
                    pc.data.name == "ou" OR
                    pc.data.name == "project" OR
                    pc.data.name == "user" OR
                    pc.data.name == "role" OR
                    pc.data.name == "user_group")
                RETURN pc
        """
        permissionContextsQueryResult = db.AQLQuery(aql, rawResults=True)
        permissionContextsResult = []
        for r in permissionContextsQueryResult:
            permissionContextsResult.append(r)

        # Create permissions with names '<action>_<permission_context>' like read_ou, create_realm ...etc
        click.echo(click.style(f"[Arango] Create permissions with names linked to permission contexts"))
        for action in ["create", "read", "update", "delete"]:
            for pc in permissionContextsResult:
                aql = """
                        UPSERT {name: @name, type: @type}
                            INSERT {_key: @id, id: @id, name: @name, type: @type, allowed_actions: ["#allowedAction"], denied_actions: []}
                            UPDATE {name: @name}
                          IN permission
                        """
                aql = aql.replace("#allowedAction", action)
                bindVars = {
                    "id": str(uuid.uuid4()),
                    "name": f'{action}_{pc["data"]["name"]}',
                    "type": "permission",
                }
                queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        click.echo(click.style(f"[Arango] Fetch all permissions"))
        aql = """
            FOR p IN permission
                RETURN p
        """
        permissionsResult = db.AQLQuery(aql, rawResults=True)

        click.echo(click.style(f"[Arango] Link permissions to permission contexts"))
        for perm in permissionsResult:
            aql = """
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'permission', _to_type: 'permission_context'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'permission', _to_type: 'permission_context'}
                  IN `for`
                """
            rtName = perm["name"][perm["name"].find("_") + 1 :]
            rtId = None
            for pc in permissionContextsResult:
                if pc["data"]["name"] == rtName:
                    rtId = pc["_id"]
                    break
            if rtId is None:
                click.echo(click.style(f"rtId is none for {rtName}", fg="red"))

            if rtId is not None:
                bindVars = {"fromId": perm["_id"], "toId": rtId}
                queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

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

    arangoClient = ArangoClient.clientByDefaultEnv()
    conn = arangoClient.getConnection()

    users = Users(connection=conn)
    click.echo(click.style("[Arango] Current users fetched", fg="green"))

    user = None
    try:
        user = users.fetchUser(username=email)
        click.echo(click.style(f"[Arango] User {email} fetched", fg="green"))
    except Exception as _e:
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


@cli.command(help="Create user and assign super admin role")
def create_arango_resource_user_with_sys_admin_role():
    click.echo(click.style(f"[Arango] Create user and assign super_admin role", fg="green"))

    arangoClient = ArangoClient.clientByDefaultEnv()
    conn = arangoClient.getConnection()

    db = conn["cafm-identity"]

    name = "sys_admin"
    title = "System Admin"
    arangoClient.createOrUpdateRole(
        db=db,
        roleName=name,
        roleTitle=title,
    )

    email = "user@admin.system"
    arangoClient.createOrUpdateUser(
        db=db,
        email=email,
        password="1234",
    )

    roleDocId = arangoClient.getResourceDocId(db, nameOrEmail=name, type="role")
    if roleDocId is None:
        raise Exception("[Arango] Something went wrong with role resource")

    userDocId = arangoClient.getResourceDocId(db, nameOrEmail=email, type="user")
    if userDocId is None:
        raise Exception("[Arango] Something went wrong with user resource")

    arangoClient.createOrUpdateHasEdge(
        db=db,
        fromId=userDocId,
        toId=roleDocId,
        fromType="user",
        toType="role",
    )


@cli.command(help="Create permission with permission contexts for the api endpoints")
def create_permission_with_permission_contexts_for_api_endpoints():
    click.echo(click.style(f"[cafm-api] Creating permission with permission contexts and linking them", fg="green"))
    cafmClient = CafmClient(
        config=CafmClientConfig(
            email=os.getenv("ADMIN_EMAIL", None),
            password=os.getenv("ADMIN_PASSWORD", None),
            baseUrl=os.getenv("API_URL"),
            cache=Cache.instance()
        )
    )

    cafmClient.creatPermissionWithPermissionContextsForApiEndpoints()

    click.echo(
        click.style(
            f"[cafm-api] Creating permission with permission contexts and linking them",
            fg="green",
        )
    )


@cli.command(help="Create user from file")
@click.argument("filename")
def build_resource_tree_from_file(filename):
    click.echo(click.style(f"[Resources] Build from tree", fg="green"))
    treeParser = TreeParser(
        cafmClient=CafmClient(
            config=CafmClientConfig(
                email=os.getenv("ADMIN_EMAIL", None),
                password=os.getenv("ADMIN_PASSWORD", None),
                baseUrl=os.getenv("API_URL"),
                cache=Cache.instance()
            )
        )
    )

    with open(f"{filename}", "r") as f:
        data = yaml.safe_load(f)
        click.echo(click.style(f"[Resources] Read data from file {filename}", fg="green"))

    try:
        click.echo(click.style(f"[Build] Resource trees", fg="green"))
        resourceTrees = data["resource_trees"]
        for resourceTreeName in resourceTrees:
            resourceTree = resourceTrees[resourceTreeName]
            click.echo(click.style(f"[Build] Resource Tree {resourceTreeName}"))
            treeParser.parseResourceTree(parent=resourceTree)

        click.echo(click.style(f"[Build] Permission trees", fg="green"))
        permissionTrees = data["permission_trees"]
        for permissionTreeName in permissionTrees:
            permissionTree = permissionTrees[permissionTreeName]
            treeParser.parsePermissionTree(permissionTree)

        click.echo(click.style(f"[Build] Role trees", fg="green"))
        roleTrees = data["role_trees"]
        for roleTreeName in roleTrees:
            roleTree = roleTrees[roleTreeName]
            treeParser.parseRoleTree(roleTree)

        click.echo(click.style(f"[Build] User trees", fg="green"))
        userTrees = data["user_trees"]
        for userTreeName in userTrees:
            userTree = userTrees[userTreeName]
            treeParser.parseUserTree(userTree)

    except Exception as e:
        currentFrame = inspect.currentframe()
        click.echo(click.style(f"Error: {currentFrame.f_code.co_name}", fg="red"))
        click.echo(click.style(f"{e}", fg="red"))
        exit(1)


if __name__ == "__main__":
    cli()
