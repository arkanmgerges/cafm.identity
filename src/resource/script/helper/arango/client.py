import click
import hashlib
import os
import uuid

from pyArango.connection import Connection
from pyArango.query import AQLQuery


class ArangoClient:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def getConnection(self):
        if self.connection != None:
            return self.connection

        try:
            self.connection = Connection(**self.config)
            return self.connection
        except Exception as e:
            raise Exception(
                f"[ArangoClient] Could not connect to database, message: {e}"
            )

    def createOrUpdateRole(self, db, roleName, roleTitle, roleId=None):
        id = roleId or str(uuid.uuid4())
        aql = """
            UPSERT {name: @name, type: @type}
                INSERT {_key: @id, id: @id, name: @name, title: @title, type: @type}
                UPDATE {name: @name, title: @title, type: @type}
                IN resource
            """
        bindVars = {
            "id": id,
            "name": roleName,
            "title": roleTitle,
            "type": "role",
        }
        query: AQLQuery = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        click.echo(click.style(f"[Arango Client] Role {roleName} upserted", fg="green"))

    def createOrUpdateUser(self, db, email, password, userId=None):
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()
        id = userId or str(uuid.uuid4())
        aql = """
            UPSERT {email: @email, type: @type}
                INSERT {id: @id, email: @email, password: @password, type: @type }
                UPDATE {email: @email, password: @password, type: @type}
                IN resource
            """
        bindVars = {
            "id": id,
            "email": email,
            "password": hashedPassword,
            "type": "user",
        }
        query: AQLQuery = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        click.echo(click.style(f"[Arango Client] User {email} upserted", fg="green"))

    def getResourceDocId(self, db, nameOrEmail, type):
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
        query: AQLQuery = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        return query.result[0]["_id"]

    def createOrUpdateHasEdge(self, db, fromId, toId, fromType, toType):
        aql = """
            UPSERT {_from: @fromId, _to: @toId}
                INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                IN has
            """
        bindVars = {
            "fromId": fromId,
            "toId": toId,
            "fromType": fromType,
            "toType": toType,
        }
        query: AQLQuery = db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        click.echo(
            click.style(
                f"[Arango Client] Edge of type 'has' from {fromType}:{fromId} to {toType}:{toId} was upserted",
                fg="green",
            )
        )
