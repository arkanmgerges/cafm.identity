"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.resource.logging.logger import logger


class ProjectRepositoryImpl(ProjectRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(
                f'[{ProjectRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')

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

    def projectById(self, id: str) -> Project:
        aql = '''
            FOR u IN project
            FILTER u.id == @id
            RETURN u
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise ProjectDoesNotExistException(name=f'project id: {id}')

        return Project.createFrom(id=result[0]['id'], name=result[0]['name'])

    def projectsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                             order: List[dict] = None) -> dict:
        sortData = ''
        if order is None:
            order = []
        else:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN project #sortData RETURN d)
                RETURN {items: SLICE(ds, @resultFrom, @resultSize), itemCount: LENGTH(ds)}
            '''
            if sortData != '':
                aql = aql.replace('#sortData', f'SORT {sortData}')
            else:
                aql = aql.replace('#sortData', '')

            bindVars = {"resultFrom": resultFrom, "resultSize": resultSize}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            result = queryResult.result
            if len(result) == 0:
                return {"items": [], "itemCount": 0}
            return {"items": [Project.createFrom(id=x['id'], name=x['name']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}

    def deleteProject(self, project: Project) -> None:
        aql = '''
            FOR d IN project
            FILTER d.id == @id
            REMOVE d IN project
        '''

        bindVars = {"id": project.id()}
        logger.debug(f'[{ProjectRepositoryImpl.deleteProject.__qualname__}] - Delete project with id: {project.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        # Check if it is deleted
        try:
            self.projectById(project.id())
            raise ObjectCouldNotBeDeletedException()
        except ProjectDoesNotExistException:
            project.publishDelete()

    def updateProject(self, project: Project) -> None:
        oldProject = self.projectById(project.id())
        if oldProject == project:
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN project
            FILTER d.id == @id
            UPDATE d WITH {name: @name} IN project
        '''

        bindVars = {"id": project.id(), "name": project.name()}
        logger.debug(f'[{ProjectRepositoryImpl.updateProject.__qualname__}] - Update project with id: {project.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        # Check if it is updated
        aProject = self.projectById(project.id())
        if aProject != project:
            raise ObjectCouldNotBeUpdatedException()
