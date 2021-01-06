"""
@author: Mohammad S. moso<moso@develoop.run>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.resource.exception.CountryDoesNotExistException import CountryDoesNotExistException
from src.domain_model.country.Country import Country
from src.domain_model.country.CountryRepository import CountryRepository
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.token.TokenData import TokenData
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class CountryRepositoryImpl(CountryRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
            self._helperRepo: HelperRepository = AppDi.instance.get(HelperRepository)
            self._policyService: PolicyControllerService = AppDi.instance.get(PolicyControllerService)
        except Exception as e:
            logger.warn(f'[{CountryRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    @debugLogger
    def countries(self, tokenData: TokenData, roleAccessPermissionData: List[RoleAccessPermissionData],
                  resultFrom: int = 0,
                  resultSize: int = 100,
                  order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        aql = '''
            LET ds = (FOR d IN country #sortData RETURN d)
            RETURN {items: ds}
        '''
        if sortData != '':
            aql = aql.replace('#sortData', f'SORT {sortData}')
        else:
            aql = aql.replace('#sortData', '')

        queryResult: AQLQuery = self._db.AQLQuery(aql, rawResults=True)
        result = queryResult.result[0]

        if result is None or len(result['items']) == 0:
            return {"items": [], "itemCount": 0}
        items = result['items']
        itemCount = len(items)
        items = items[resultFrom:resultSize]
        return {"items": [Country.createFrom(id=x['id'], geoNameId=x['geo_name_id'], localeCode=x['locale_code'],
                                             continentCode=x['continent_code'], continentName=x['continent_name'],
                                             countryIsoCode=x['country_iso_code'], countryName=x['country_name'],
                                             isInEuropeanUnion=x['is_in_european_union']) for x in
                          items],
                "itemCount": itemCount}

    @debugLogger
    def countryById(self, id: str) -> Country:
        aql = '''
            FOR d IN country
                FILTER d.id == @id
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{CountryRepositoryImpl.countryById.__qualname__}] country id: {id}')
            raise CountryDoesNotExistException(f'country id: {id}')
        return Country.createFrom(id=result[0]['id'], geoNameId=result[0]['geo_name_id'],
                                  localeCode=result[0]['locale_code'], continentCode=result[0]['continent_code'],
                                  continentName=result[0]['continent_name'],
                                  countryIsoCode=result[0]['country_iso_code'], countryName=result[0]['country_name'],
                                  isInEuropeanUnion=result[0]['is_in_european_union'])
