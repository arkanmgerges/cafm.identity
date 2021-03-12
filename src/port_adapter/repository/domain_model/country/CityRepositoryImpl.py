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
                    LET ds = (FOR d IN city #sortData LIMIT @resultFrom, @resultSize RETURN d)
                    LET length = (FOR doc IN city COLLECT WITH COUNT INTO length RETURN length)
                    RETURN {items: ds, count: length}
                '''
        if sortData != '':
            aql = aql.replace('#sortData', f'SORT {sortData}')
        else:
            aql = aql.replace('#sortData', '')
        bindVars = {"resultFrom": resultFrom, 'resultSize': resultFrom + resultSize}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result[0]

        if result is None or len(result['items']) == 0:
            return {"items": [], "itemCount": 0}
        items = result['items']
        itemCount = result['count'][0]
        # items = items[resultFrom:resultFrom + resultSize]

        returnItems = []
        for x in items:
            cityName = x['city_name'] if 'city_name' in x else ''
            subdivisionOneIsoCode = x['subdivision_1_iso_code'] if 'subdivision_1_iso_code' in x else ''
            subdivisionOneIsoName = x['subdivision_1_name'] if 'subdivision_1_name' in x else ''
            returnItems.append(City.createFrom(id=x['geoname_id'], localeCode=x['locale_code'],
                                               continentCode=x['continent_code'], cityName=cityName,
                                               subdivisionOneIsoCode=subdivisionOneIsoCode,
                                               subdivisionOneIsoName=subdivisionOneIsoName,
                                               continentName=x['continent_name'], countryIsoCode=x['country_iso_code'],
                                               countryName=x['country_name'], timeZone=x['time_zone'],
                                               isInEuropeanUnion=x['is_in_european_union']))
        return {"items": returnItems,
                "itemCount": itemCount}

    @debugLogger
    def cityById(self, id: str) -> City:
        aql = '''
            FOR d IN city
                FILTER d.geoname_id == @id
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{CityRepositoryImpl.cityById.__qualname__}] country id: {id}')
            raise CountryDoesNotExistException(f'city id: {id}')
        cityName = result[0]['city_name'] if 'city_name' in result[0] else ''
        subdivisionOneIsoCode = result[0]['subdivision_1_iso_code'] if 'subdivision_1_iso_code' in result[0] else ''
        subdivisionOneIsoName = result[0]['subdivision_1_name'] if 'subdivision_1_name' in result[0] else ''
        return City.createFrom(id=result[0]['geoname_id'], localeCode=result[0]['locale_code'],
                               continentCode=result[0]['continent_code'], continentName=result[0]['continent_name'],
                               countryIsoCode=result[0]['country_iso_code'], countryName=result[0]['country_name'],
                               subdivisionOneIsoCode=subdivisionOneIsoCode, subdivisionOneIsoName=subdivisionOneIsoName,
                               cityName=cityName, timeZone=result[0]['time_zone'],
                               isInEuropeanUnion=result[0]['is_in_european_union'])

    def citiesByStateId(self, id: str, resultFrom: int = 0, resultSize: int = 100, order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        aql = '''
            LET ds = (FOR d IN city
                        FILTER d.subdivision_1_iso_code == @id
                        #sortData 
                        RETURN d)
            RETURN {items: ds}
        '''
        if sortData != '':
            aql = aql.replace('#sortData', f'SORT {sortData}')
        else:
            aql = aql.replace('#sortData', '')
        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result[0]

        if result is None or len(result['items']) == 0:
            return {"items": [], "itemCount": 0}
        items = result['items']
        itemCount = len(items)
        items = items[resultFrom:resultFrom + resultSize]

        returnItems = []
        for x in items:
            cityName = x['city_name'] if 'city_name' in x else ''
            subdivisionOneIsoCode = x['subdivision_1_iso_code'] if 'subdivision_1_iso_code' in x else ''
            subdivisionOneIsoName = x['subdivision_1_name'] if 'subdivision_1_name' in x else ''
            returnItems.append(City.createFrom(id=x['geoname_id'], localeCode=x['locale_code'],
                                               continentCode=x['continent_code'], cityName=cityName,
                                               subdivisionOneIsoCode=subdivisionOneIsoCode,
                                               subdivisionOneIsoName=subdivisionOneIsoName,
                                               continentName=x['continent_name'], countryIsoCode=x['country_iso_code'],
                                               countryName=x['country_name'], timeZone=x['time_zone'],
                                               isInEuropeanUnion=x['is_in_european_union']))
        return {"items": returnItems,
                "itemCount": itemCount}
