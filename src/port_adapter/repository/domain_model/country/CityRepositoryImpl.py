"""
@author: Mohammad S. moso<moso@develoop.run>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.country.City import City
from src.domain_model.country.CityRepository import CityRepository
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.resource.exception.CountryDoesNotExistException import CountryDoesNotExistException
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class CityRepositoryImpl(CityRepository):
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
            logger.warn(f'[{CityRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    @debugLogger
    def cities(self, resultFrom: int = 0, resultSize: int = 100, order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        aql = '''
                    LET ds = (FOR d IN city #sortData RETURN d)
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
        return {"items": [City.createFrom(id=x['id'], geoNameId=x['geo_name_id'], localeCode=x['locale_code'],
                                          continentCode=x['continent_code'], continentName=x['continent_name'],
                                          countryIsoCode=x['country_iso_code'], countryName=x['country_name'],
                                          subdivisionOneIsoCode=x['subdivision_one_iso_code'],
                                          subdivisionOneIsoName=x['subdivision_one_iso_name'],
                                          subdivisionTwoIsoCode=x['subdivision_two_iso_code'],
                                          subdivisionTwoIsoName=x['subdivision_two_iso_name'],
                                          cityName=x['city_name'],
                                          metroCode=x['metro_code'], timeZone=x['time_zone'],
                                          isInEuropeanUnion=x['is_in_european_union']) for x in items],
                "itemCount": itemCount}

    @debugLogger
    def cityById(self, id: str) -> City:
        aql = '''
            FOR d IN city
                FILTER d.id == @id
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{CityRepositoryImpl.cityById.__qualname__}] country id: {id}')
            raise CountryDoesNotExistException(f'city id: {id}')
        return City.createFrom(id=result[0]['id'], geoNameId=result[0]['geo_name_id'],
                               localeCode=result[0]['locale_code'], continentCode=result[0]['continent_code'],
                               continentName=result[0]['continent_name'], countryIsoCode=result[0]['country_iso_code'],
                               countryName=result[0]['country_name'],
                               subdivisionOneIsoCode=result[0]['subdivision_one_iso_code'],
                               subdivisionOneIsoName=result[0]['subdivision_one_iso_name'],
                               subdivisionTwoIsoCode=result[0]['subdivision_two_iso_code'],
                               subdivisionTwoIsoName=result[0]['subdivision_two_iso_name'],
                               cityName=result[0]['city_name'], metroCode=result[0]['metro_code'],
                               timeZone=result[0]['time_zone'], isInEuropeanUnion=result[0]['is_in_european_union'])
