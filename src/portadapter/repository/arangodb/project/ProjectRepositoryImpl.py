"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from pyArango.query import AQLQuery

from src.domainmodel.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.domainmodel.project.Project import Project
from src.domainmodel.project.ProjectRepository import ProjectRepository

from pyArango.connection import *


class ProjectRepositoryImpl(ProjectRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CORAL_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CORAL_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CORAL_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CORAL_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(f'[ProjectRepository::__init__] Could not connect to the db, message: {e}')

    def createProject(self, project: Project):
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name}
            UPDATE {name: @name}
          IN project
        '''

        bindVars = {"id": project.id(), "name": project.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        print(queryResult)

    def projectByName(self, name: str) -> Project:
        aql = '''
            FOR u IN project
            FILTER u.name == @name
            RETURN u
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise ProjectDoesNotExistException(name)

        return Project.createFrom(id=result[0]['id'], name=result[0]['name'])
