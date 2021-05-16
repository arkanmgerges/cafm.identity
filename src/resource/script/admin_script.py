"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import sys
from time import sleep

sys.path.append("../../../")

import hashlib
import os
import uuid
import yaml
import click
from confluent_kafka.avro import CachedSchemaRegistryClient
from pyArango.connection import Connection
from pyArango.query import AQLQuery
from pyArango.users import Users
from confluent_kafka.admin import AdminClient, NewTopic

from src.port_adapter.messaging.common.model.IdentityCommand import IdentityCommand
from src.port_adapter.messaging.common.model.IdentityEvent import IdentityEvent


@click.group()
def cli():
    pass


# @cli.command()
# @click.option('--count', '-c', default=1, help='number of greetings')
# @click.argument('name')
# def hello(count, name):
#     for x in range(count):
#         click.echo(click.style('Hello %s!' % name, fg='green'))


@cli.command(help="Initialize a database")
def init_db():
    click.echo(click.style("Initialized the database", fg="green", bold=True))
    try:
        dbName = os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", None)
        if dbName is None:
            raise Exception("Db name is not set")

        connection = dbClientConnection()
        click.echo(click.style(f"Create database {dbName} if not exist", fg="green"))

        sleepPeriod = 1
        for i in range(30):
            if not connection.hasDatabase(dbName):
                connection.createDatabase(name=dbName)
                connection.reload()
                sleep(sleepPeriod)
                sleepPeriod += 3
            else:
                break

        dbConnection = connection[dbName]
        click.echo(click.style(f"Create collections:", fg="green"))
        collections = [
            "resource",
            "permission",
            "permission_context",
            "country",
            "city",
        ]
        for colName in collections:
            if not dbConnection.hasCollection(colName):
                dbConnection.createCollection(name=colName, keyOptions={"type": "uuid", "allowUserKeys": True})

        # Create edges
        click.echo(click.style(f"Create edges:", fg="green"))
        edges = ["has", "for", "access", "owned_by"]
        for edgeName in edges:
            if not dbConnection.hasCollection(edgeName):
                dbConnection.createCollection(
                    className="Edges",
                    name=edgeName,
                    keyOptions={"type": "uuid", "allowUserKeys": True},
                )

        # Add permission contexts
        permissionContextResourceNames = [
            "realm",
            "ou",
            "project",
            "user",
            "role",
            "user_group",
        ]
        click.echo(click.style(f"Create permission contexts", fg="green"))
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
            queryResult = dbConnection.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        # Add default permissions (this was added later in code. It will read the already created permission contexts and
        # create permissions for them)
        # Fetch all permission contexts
        aql = """
            FOR pc IN permission_context
                RETURN pc
        """
        permissionContextsQueryResult = dbConnection.AQLQuery(aql, rawResults=True)
        permissionContextsResult = []
        for r in permissionContextsQueryResult:
            permissionContextsResult.append(r)

        # Create permissions with names '<action>_<permission_context>' like read_ou, create_realm ...etc
        click.echo(
            click.style(
                f"Create permissions with names linked to permission contexts",
                fg="green",
            )
        )
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
                queryResult = dbConnection.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        # Fetch all permissions
        aql = """
            FOR p IN permission
                RETURN p
        """
        permissionsResult = dbConnection.AQLQuery(aql, rawResults=True)

        # Link the permissions with the permission contexts
        click.echo(click.style(f"Link permissions to permission contexts", fg="green"))
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
                click.echo(
                    click.style(
                        f"rtId is none for {rtName} and {permissionContextsResult}",
                        fg="red",
                    )
                )
            if rtId is not None:
                bindVars = {"fromId": perm["_id"], "toId": rtId}
                queryResult = dbConnection.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    except Exception as e:
        click.echo(click.style(str(e), fg="red"))
        exit(0)


@cli.command(help="Drop a database")
def drop_db():
    click.echo(click.style("Dropping the database", fg="green", bold=True))
    dbName = os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", None)
    if dbName is None:
        raise Exception("Db name is not set")

    connection = dbClientConnection()
    if connection.hasDatabase(dbName):
        "use dbArgs for arguments other than name. for a full list of arguments please have a look at arangoDB's doc"
        url = f"{connection.getURL()}/database/{dbName}"
        connection.session.delete(url)


@cli.command(help="Create an admin user for the database")
@click.argument("email")
@click.argument("password")
@click.argument("database_name")
def create_user(email, password, database_name):
    click.echo(
        click.style(
            f"Creating an admin user email: {email} for the database: {database_name}",
            fg="green",
        )
    )
    conn = dbClientConnection()
    users = Users(connection=conn)
    try:
        users.fetchUser(email)
        user = users.createUser(email, password)
        user.save()
        user.setPermissions(dbName=database_name, access=True)
    except:
        pass


@cli.command(help="Delete a user from the database")
@click.argument("email")
@click.argument("database_name")
def delete_user(email, database_name):
    click.echo(
        click.style(
            f"Deleting user email: {email} from the database: {database_name}",
            fg="green",
        )
    )
    conn = dbClientConnection()
    users = Users(connection=conn)
    user = users.fetchUser(email)
    user.delete()


@cli.command(help="Create user document and assign it a super admin role in database")
@click.argument("email")
@click.argument("password")
@click.argument("database_name")
def assign_user_super_admin_role(email, password, database_name):
    click.echo(
        click.style(
            f"Creating user email: {email} document in the database: {database_name} and assigning a super admin role",
            fg="green",
        )
    )
    conn = dbClientConnection()
    db = conn[database_name]

    # Creating a user
    userId = str(uuid.uuid4())
    createUser(db, userId, email, password)

    # Get the user doc id
    userDocId = resourceDocId(db, email, "user")

    # Create a role
    roleId = str(uuid.uuid4())
    createResource(db, roleId, "super_admin", "role")

    # Get the role doc id
    roleDocId = resourceDocId(db, "super_admin", "role")

    # Assign a role to the user
    assignParentToChildResource(db, userDocId, roleDocId, "user", "role")


@cli.command(help="Create resources with user and role from file")
@click.argument("file_name")
def build_resource_tree_from_file(file_name):
    fileData = None
    with open(f"{file_name}", "r") as f:
        fileData = yaml.safe_load(f)

    databaseName = fileData["database_name"]
    conn = dbClientConnection()
    db = conn[databaseName]

    # Parse access tree
    for treeNode in fileData["tree"]:
        # Parse the tree
        addNode(db=db, parent=treeNode, children=treeNode["children"])

    for user in fileData["users"]:
        email = user["email"]
        password = user["password"]
        click.echo(
            click.style(
                f"Creating user email: {email} document in the database: {databaseName} and assigning a super admin role",
                fg="green",
            )
        )

        id = str(uuid.uuid4())
        createUser(db, id, email, password)
        userDocId = resourceDocId(db, email, "user")
        roles = user["roles"]
        for role in roles:
            id = str(uuid.uuid4())
            createResource(db, id, role["name"], "role")
            roleDocId = resourceDocId(db, role["name"], "role")
            for permission in role["permissions"]:
                permDocId = permissionDocId(db, permission["name"])
                assignParentToChildResource(db, roleDocId, permDocId, "role", "permission")
            # Assign access for the role to the tree
            for treeNode in role["access"]:
                docId = resourceDocId(db, treeNode["name"], treeNode["type"])
                assignRoleAccessToResource(db, roleDocId, docId, "role", treeNode["type"])

            # Assign role to user
            assignParentToChildResource(db, userDocId, roleDocId, "user", "role")


def addNode(db=None, parent=None, children=None):
    parentDocId = None
    if parent is not None:
        id = str(uuid.uuid4())
        createResource(db, id, parent["name"], parent["type"])
        parentDocId = resourceDocId(db, parent["name"], parent["type"])
    for childNode in children:
        id = str(uuid.uuid4())
        createResource(db, id, childNode["name"], childNode["type"])

        addNode(db, childNode, childNode["children"])

        childDocId = resourceDocId(db, childNode["name"], childNode["type"])
        if parent is not None:
            assignParentToChildResource(db, parentDocId, childDocId, parent["type"], childNode["type"])


# def addNode(db, node):
#     # Get the user doc id
#     id = uuid.uuid4()
#     createResource(db, id, node['name'], node['type'])
#     docId = resourceDocId(db, node['name'], node['type'])
#
#     for childNode in node['children']:
#         addNode(db, childNode)
#         childDocId = resourceDocId(db, childNode['name'], childNode['type'])
#         assignParentToChildResource(db, docId, childDocId, node['type'], childNode['type'])


def assignParentToChildResource(db, fromId, toId, fromType, toType):
    aql = """
            UPSERT {_from: @fromId, _to: @toId}
                INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
              IN has                  
            """
    bindVars = {"fromId": fromId, "toId": toId, "fromType": fromType, "toType": toType}
    queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)


def assignRoleAccessToResource(db, fromId, toId, fromType, toType):
    aql = """
            UPSERT {_from: @fromId, _to: @toId}
                INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
              IN `access`                  
            """
    bindVars = {"fromId": fromId, "toId": toId, "fromType": fromType, "toType": toType}
    queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)


def createResource(db, id, nameOrEmail, type):
    if type == "user":
        aql = """
            UPSERT {email: @nameOrEmail, type: @type}
                INSERT {id: @id, email: @nameOrEmail, type: @type}
                UPDATE {email: @nameOrEmail, type: @type}
              IN resource
            """
    else:
        aql = """
            UPSERT {name: @nameOrEmail, type: @type}
                INSERT {id: @id, name: @nameOrEmail, type: @type}
                UPDATE {name: @nameOrEmail, type: @type}
              IN resource
            """

    bindVars = {"id": id, "nameOrEmail": nameOrEmail, "type": type}
    queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)


def resourceDocId(db, nameOrEmail, type):
    aql = """
        FOR r IN resource
        FILTER r.name == @name AND r.type == @type
        RETURN r
    """

    if type == "user":
        aql = """
            FOR r IN resource
            FILTER r.email == @nameOrEmail AND r.type == @type
            RETURN r
            """
    else:
        aql = """
            FOR r IN resource
            FILTER r.name == @nameOrEmail AND r.type == @type
            RETURN r
            """
    bindVars = {"nameOrEmail": nameOrEmail, "type": type}
    queryResult: AQLQuery = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
    result = queryResult.result[0]
    return result["_id"]


def permissionDocId(db, name):
    aql = """
        FOR p IN permission
        FILTER p.name == @name AND p.type == "permission"
        RETURN p
    """

    bindVars = {"name": name}
    queryResult: AQLQuery = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
    result = queryResult.result[0]
    return result["_id"]


def createUser(db, id, email, password):
    password = hashlib.sha256(password.encode()).hexdigest()
    aql = """
            UPSERT {email: @email, type: 'user'}
                INSERT {id: @id,
                        email: @email,
                        password: @password,
                        type: 'user'}
                UPDATE {email: @email, password: @password, type: 'user'}
              IN resource
            """
    bindVars = {"id": id, "email": email, "password": password}
    queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)


@cli.command(help="Initialize kafka topics and schema registries")
def init_kafka_topics_and_schemas():
    # Create topics
    requiredTopics = [
        "cafm.identity.cmd",
        "cafm.identity.evt",
        "cafm.identity.api-failed-cmd-handle",
        "cafm.identity.failed-cmd-handle",
        "cafm.identity.failed-evt-handle",
        "cafm.identity.project-failed-evt-handle",
    ]
    click.echo(click.style(f"Initializing kafka topics and schema registries", fg="green"))
    newTopics = []
    admin = AdminClient({"bootstrap.servers": os.getenv("MESSAGE_BROKER_SERVERS", "")})
    installedTopics = admin.list_topics().topics.keys()

    for requiredTopic in requiredTopics:
        if requiredTopic not in installedTopics:
            newTopics.append(
                NewTopic(
                    requiredTopic,
                    num_partitions=int(os.getenv("KAFKA_PARTITIONS_COUNT_PER_TOPIC", 1)),
                    replication_factor=1,
                )
            )

    if len(newTopics) > 0:
        fs = admin.create_topics(newTopics)
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                click.echo(click.style("Topic {} created".format(topic), fg="green"))
            except Exception as e:
                click.echo(click.style(f"Failed to create topic {topic}: {e}", fg="red"))

    # Create schemas
    c = CachedSchemaRegistryClient({"url": os.getenv("MESSAGE_SCHEMA_REGISTRY_URL", "")})
    requiredSchemas = [
        {"name": "cafm.identity.Command", "schema": IdentityCommand.get_schema()},
        {"name": "cafm.identity.Event", "schema": IdentityEvent.get_schema()},
    ]
    newSchemas = []
    for requiredSchema in requiredSchemas:
        click.echo(click.style(f'Verify if schema {requiredSchema["name"]} is available', fg="green"))
        r = c.get_latest_schema(subject=f'{requiredSchema["name"]}')
        if r[0] is None:
            click.echo(click.style(f'Schema {requiredSchema["name"]} will be created', fg="green"))
            newSchemas.append(requiredSchema)
    [c.register(schema["name"], schema["schema"]) for schema in newSchemas]


@cli.command(help="Drop kafka topics and schema registries")
def drop_kafka_topics_and_schemas():
    # Delete topics
    topics = [
        "cafm.identity.cmd",
        "cafm.identity.evt",
        "cafm.identity.api-failed-cmd-handle",
        "cafm.identity.failed-cmd-handle",
        "cafm.identity.failed-evt-handle",
        "cafm.identity.project-failed-evt-handle",
    ]
    click.echo(click.style(f"Dropping kafka topics and schema registries", fg="green"))
    admin = AdminClient({"bootstrap.servers": os.getenv("MESSAGE_BROKER_SERVERS", "")})
    fs = admin.delete_topics(topics, operation_timeout=30)
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            click.echo(click.style("Topic {} deleted".format(topic), fg="green"))
        except Exception as e:
            click.echo(click.style(f"Failed to delete topic {topic}: {e}", fg="red"))

    # Delete schemas
    schemas = ["cafm.identity.Command", "cafm.identity.Event"]
    c = CachedSchemaRegistryClient({"url": os.getenv("MESSAGE_SCHEMA_REGISTRY_URL", "")})
    [c.delete_subject(schema) for schema in schemas]


@cli.command(help="Check if schema registry is ready")
def check_schema_registry_readiness():
    from confluent_kafka.avro import CachedSchemaRegistryClient

    click.echo(click.style("Check if schema registry is ready", fg="green", bold=True))
    counter = 15
    sleepPeriod = 10
    while counter > 0:
        try:
            counter -= 1
            click.echo(click.style("Sending a request ...", fg="green", bold=True))
            c = CachedSchemaRegistryClient({"url": os.getenv("MESSAGE_SCHEMA_REGISTRY_URL", "")})
            c.get_latest_schema(subject="test")
            click.echo(click.style("Schema registry is ready", fg="green", bold=True))
            exit(0)
        except Exception as e:
            click.echo(click.style(f"Error thrown ... {e}", fg="red"))
            click.echo(click.style(f"Sleep {sleepPeriod} seconds ...", fg="green", bold=True))
            click.echo(click.style(f"Remaining retries: {counter}", fg="green"))
            sleepPeriod += 3
            sleep(sleepPeriod)
    exit(1)


@cli.command(help="Check if redis is ready")
def check_redis_readiness():
    import redis
    from redis.client import Redis

    click.echo(click.style("Check if redis is ready", fg="green", bold=True))
    counter = 15
    sleepPeriod = 10
    while counter > 0:
        try:
            counter -= 1
            cache: Redis = redis.Redis(
                host=os.getenv("CAFM_IDENTITY_REDIS_HOST", "localhost"),
                port=os.getenv("CAFM_IDENTITY_REDIS_PORT", 6379),
            )
            cache.setex("test_redis_key", 10, "test")
            if cache.exists("test_redis_key"):
                click.echo(click.style("redis is ready", fg="green", bold=True))
                exit(0)
            sleepPeriod += 3
            sleep(sleepPeriod)
        except Exception as e:
            click.echo(click.style(f"Error thrown ... {e}", fg="red"))
            click.echo(click.style(f"Sleep {sleepPeriod} seconds ...", fg="green", bold=True))
            click.echo(click.style(f"Remaining retries: {counter}", fg="green"))
            sleepPeriod += 3
            sleep(sleepPeriod)
    exit(1)


def dbClientConnection():
    try:
        connection = Connection(
            arangoURL=os.getenv("CAFM_IDENTITY_ARANGODB_URL", ""),
            username=os.getenv("CAFM_IDENTITY_ARANGODB_USERNAME", ""),
            password=os.getenv("CAFM_IDENTITY_ARANGODB_PASSWORD", ""),
        )
        return connection
    except Exception as e:
        raise Exception(f"Could not connect to the db, message: {e}")


if __name__ == "__main__":
    cli()
