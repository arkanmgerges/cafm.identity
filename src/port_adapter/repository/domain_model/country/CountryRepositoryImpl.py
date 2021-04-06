"""
@author: Mohammad S. moso<moso@develoop.run>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.country.City import City
from src.domain_model.country.Country import Country
from src.domain_model.country.CountryRepository import CountryRepository
from src.domain_model.country.State import State
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.resource.exception.CountryDoesNotExistException import CountryDoesNotExistException
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
    def countries(self, resultFrom: int = 0, resultSize: int = 100, order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        aql = '''
            LET ds = (FOR d IN country 
                          FILTER d.country_iso_code != null AND d.country_iso_code != ""
                          #sortData RETURN d)
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
        items = items[resultFrom:resultFrom + resultSize]
        return {"items": [Country.createFrom(id=x['geoname_id'], localeCode=x['locale_code'],
                                             continentCode=x['continent_code'], continentName=x['continent_name'],
                                             countryIsoCode=x['country_iso_code'], countryName=x['country_name'],
                                             isInEuropeanUnion=x['is_in_european_union']) for x in items],
                "itemCount": itemCount}

    @debugLogger
    def countryById(self, id: int) -> Country:
        aql = '''
            FOR d IN country
                FILTER d.geoname_id == @id
                FILTER d.country_iso_code != null AND d.country_iso_code != ""
                RETURN d
        '''
        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{CountryRepositoryImpl.countryById.__qualname__}] country id: {id}')
            raise CountryDoesNotExistException(f'country id: {id}')
        return Country.createFrom(id=result[0]['geoname_id'],
                                  localeCode=result[0]['locale_code'], continentCode=result[0]['continent_code'],
                                  continentName=result[0]['continent_name'],
                                  countryIsoCode=result[0]['country_iso_code'], countryName=result[0]['country_name'],
                                  isInEuropeanUnion=result[0]['is_in_european_union'])

    @debugLogger
    def citiesByCountryId(self, id: int = '', resultFrom: int = 0, resultSize: int = 100,
                          order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        aql = '''
            LET ds = (FOR u IN country 
                        FOR c IN city 
                            FILTER u.country_iso_code == c.country_iso_code 
                            FILTER u.geoname_id == @id 
                            FILTER c.city_name != null AND c.city_name != ""
                            #sortData
                            RETURN c)
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

        return {"items": [City.createFrom(id=x['geoname_id'], localeCode=x['locale_code'],
                                          continentCode=x['continent_code'], continentName=x['continent_name'],
                                          countryIsoCode=x['country_iso_code'], countryName=x['country_name'],
                                          subdivisionOneIsoCode=x[
                                              'subdivision_1_iso_code'] if 'subdivision_1_iso_code' in x else '',
                                          subdivisionOneIsoName=x[
                                              'subdivision_1_name'] if 'subdivision_1_name' in x else '',
                                          cityName=x['city_name'],
                                          timeZone=x['time_zone'], isInEuropeanUnion=x['is_in_european_union']) for x in
                          items],
                "itemCount": itemCount}

    @debugLogger
    def cityByCountryId(self, countryId: int = '', cityId: int = '') -> City:
        aql = '''
            FOR u IN country 
                FOR c IN city 
                    FILTER u.country_iso_code == c.country_iso_code 
                    FILTER u.geoname_id == @countryID
                    FILTER c.geoname_id == @cityID 
                    RETURN c
                    
        '''

        bindVars = {"countryID": countryId, "cityID": cityId}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        if len(result) == 0:
            logger.debug(
                f'[{CountryRepositoryImpl.cityByCountryId.__qualname__}] country id: {countryId}, city id: {cityId}')
            raise CountryDoesNotExistException(f'country id: {countryId}, city id: {cityId}')

        return City.createFrom(id=result[0]['geoname_id'], localeCode=result[0]['locale_code'],
                               continentCode=result[0]['continent_code'], continentName=result[0]['continent_name'],
                               countryIsoCode=result[0]['country_iso_code'], countryName=result[0]['country_name'],
                               subdivisionOneIsoCode=result[0]['subdivision_1_iso_code'],
                               subdivisionOneIsoName=result[0]['subdivision_1_name'],
                               cityName=result[0]['city_name'], timeZone=result[0]['time_zone'],
                               isInEuropeanUnion=result[0]['is_in_european_union'])

    @debugLogger
    def statesByCountryId(self, id: int = 0, resultFrom: int = 0, resultSize: int = 100,
                          order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, c.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        aql = '''
                    LET ds = (FOR u IN country 
                                FOR c IN city 
                                    FILTER u.country_iso_code == c.country_iso_code 
                                    FILTER u.geoname_id == @id 
                                    FILTER c.subdivision_1_iso_code != null AND c.subdivision_1_iso_code != ""
                                    #sortData
                                    RETURN c)
                    
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
        items = []
        duplicate = []
        for item in result['items']:
            if item['subdivision_1_iso_code'] not in duplicate:
                items.append(item)
                duplicate.append(item['subdivision_1_iso_code'])
        itemCount = len(items)
        items = items[resultFrom:resultFrom + resultSize]

        return {"items": [State.createFrom(id=str(x['subdivision_1_iso_code']), name=x['subdivision_1_name'])
                          for x in items],
                "itemCount": itemCount}
