"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import sys
sys.path.append("../../../")

import hashlib
import os
import uuid

import click
from confluent_kafka.avro import CachedSchemaRegistryClient
from pyArango.connection import Connection
from pyArango.query import AQLQuery
from pyArango.users import Users
from confluent_kafka.admin import AdminClient, NewTopic


from src.port_adapter.messaging.common.model.ApiCommand import ApiCommand
from src.port_adapter.messaging.common.model.ApiResponse import ApiResponse
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


@cli.command(help='Initialize a database')
def init_db():
    click.echo(click.style('Initialized the database', fg='green', bold=True))
    try:
        dbName = os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', None)
        if dbName is None:
            raise Exception('Db name is not set')

        connection = dbClientConnection()
        click.echo(click.style(f'Create database {dbName} if not exist', fg='green'))
        if not connection.hasDatabase(dbName):
            connection.createDatabase(name=dbName)

        dbConnection = connection[dbName]
        click.echo(click.style(f'Create collections:', fg='green'))
        collections = ['project', 'user_group', 'user', 'permission', 'role', 'resource_type', 'realm', 'ou']
        with click.progressbar(collections) as colBar:
            for colName in colBar:
                if not dbConnection.hasCollection(colName):
                    dbConnection.createCollection(name=colName)

        # Add resource types
        for resourceType in ['realm', 'ou', 'project', 'user', 'role', 'permission']:
            aql = '''
                        UPSERT { name: @name}
                            INSERT {id: @id, name: @name}
                            UPDATE {name: @name}
                          IN resource_type
                        '''

            bindVars = {"id": uuid.uuid4(), "name": resourceType}
            queryResult = dbConnection.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        # Create edges
        click.echo(click.style(f'Create edges:', fg='green'))
        edges = ['has', 'for', 'access']
        with click.progressbar(edges) as edgeBar:
            for edgeName in edgeBar:
                if not dbConnection.hasCollection(colName):
                    dbConnection.createCollection(className='Edges', name=edgeName)
    except Exception as e:
        click.echo(click.style(str(e), fg='red'))
        exit(0)


@cli.command(help='Drop a database')
def drop_db():
    click.echo(click.style('Dropping the database', fg='green', bold=True))
    dbName = os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', None)
    if dbName is None:
        raise Exception('Db name is not set')

    connection = dbClientConnection()
    if connection.hasDatabase(dbName):
        "use dbArgs for arguments other than name. for a full list of arguments please have a look at arangoDB's doc"
        url = f'{connection.getURL()}/database/{dbName}'
        connection.session.delete(url)


@cli.command(help='Create an admin user for the database')
@click.argument('username')
@click.argument('password')
@click.argument('database_name')
def create_user(username, password, database_name):
    click.echo(click.style(f'Creating an admin user: {username} for the database: {database_name}', fg='green'))
    conn = dbClientConnection()
    users = Users(connection=conn)
    user = users.createUser(username, password)
    user.save()
    user.setPermissions(dbName=database_name, access=True)


@cli.command(help='Delete a user from the database')
@click.argument('username')
@click.argument('database_name')
def delete_user(username, database_name):
    click.echo(click.style(f'Deleting user: {username} from the database: {database_name}', fg='green'))
    conn = dbClientConnection()
    users = Users(connection=conn)
    user = users.fetchUser(username)
    user.delete()

@cli.command(help='Create user document and assign it a super admin role in database')
@click.argument('username')
@click.argument('password')
@click.argument('database_name')
def assign_user_super_admin_role(username, password, database_name):
    click.echo(click.style(f'Creating user: {username} document in the database: {database_name} and assigning a super admin role', fg='green'))
    conn = dbClientConnection()
    db = conn[database_name]

    # Creating a user
    userId = uuid.uuid4()
    password = hashlib.sha256(password.encode()).hexdigest()
    aql = '''
            UPSERT { name: @name}
                INSERT {id: @id, name: @name, password: @password}
                UPDATE {name: @name, password: @password }
              IN user
            '''

    bindVars = {"id": userId, "name": username, "password": password}
    queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    # Get the user doc id
    aql = '''
                FOR u IN user
                FILTER u.name == @name
                RETURN u
            '''

    bindVars = {"name": username}
    queryResult: AQLQuery = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
    result = queryResult.result[0]
    userDocId = result['_id']

    # Create a super admin role
    aql = '''
            UPSERT { name: @name}
                INSERT {id: @id, name: @name}
                UPDATE {name: @name}
              IN role
            '''
    roleId = uuid.uuid4()
    bindVars = {"id": roleId, "name": 'super_admin'}
    queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    # Get the role doc id
    aql = '''
                    FOR r IN role
                    FILTER r.name == 'super_admin'
                    RETURN r
                '''

    queryResult: AQLQuery = db.AQLQuery(aql, rawResults=True)
    result = queryResult.result[0]
    roleDocId = result['_id']

    # Assign super admin role to the user
    aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, from_type: 'user', to_type: 'role'}
                    UPDATE {_from: @fromId, _to: @toId, from_type: 'user', to_type: 'role'}
                  IN has                  
                '''
    bindVars = {"fromId": userDocId, "toId": roleDocId}
    queryResult = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

@cli.command(help='Initialize kafka topics and schema registries')
def init_kafka():
    # Create topics
    topics = ['cafm.api.cmd', 'cafm.api.rsp', 'cafm.identity.cmd', 'cafm.identity.evt']
    newTopics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]
    admin = AdminClient({'bootstrap.servers': os.getenv('MESSAGE_BROKER_SERVERS', '')})
    fs = admin.create_topics(newTopics)
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            click.echo(click.style("Topic {} created".format(topic), fg='green'))
        except Exception as e:
            click.echo(click.style(f'Failed to create topic {topic}: {e}', fg='red'))

    # Create schemas
    c = CachedSchemaRegistryClient({'url': os.getenv('MESSAGE_SCHEMA_REGISTRY_URL', '')})
    schemas = [{'name': 'cafm.api.Command', 'schema': ApiCommand.get_schema()},
               {'name': 'cafm.api.Response', 'schema': ApiResponse.get_schema()},
               {'name': 'cafm.identity.Command', 'schema': IdentityCommand.get_schema()},
               {'name': 'cafm.identity.Event', 'schema': IdentityEvent.get_schema()}]
    [c.register(schema['name'], schema['schema']) for schema in schemas]


@cli.command(help='Drop kafka topics and schema registries')
def drop_kafka():
    # Delete topics
    topics = ['cafm.api.cmd', 'cafm.api.rsp', 'cafm.identity.cmd', 'cafm.identity.evt']
    admin = AdminClient({'bootstrap.servers': os.getenv('MESSAGE_BROKER_SERVERS', '')})
    fs = admin.delete_topics(topics, operation_timeout=30)
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            click.echo(click.style("Topic {} deleted".format(topic), fg='green'))
        except Exception as e:
            click.echo(click.style(f'Failed to delete topic {topic}: {e}', fg='red'))

    # Delete schemas
    schemas = ['cafm.api.Command', 'cafm.api.Response', 'cafm.identity.Command', 'cafm.identity.Event']
    c = CachedSchemaRegistryClient({'url': os.getenv('MESSAGE_SCHEMA_REGISTRY_URL', '')})
    [c.delete_subject(schema) for schema in schemas]



def dbClientConnection():
    try:
        connection = Connection(
            arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
            username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
            password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
        )
        return connection
    except Exception as e:
        raise Exception(f'Could not connect to the db, message: {e}')


if __name__ == '__main__':
    cli()
