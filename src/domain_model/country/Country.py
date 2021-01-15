"""
@author: Mohammad S. moso<moso@develoop.run>
"""
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.resource.logging.logger import logger


class Country(Resource):
    def __init__(self, geoNameId: str = '', localeCode: str = '', continentCode: str = '',
                 continentName: str = '', countryIsoCode: str = '', countryName: str = '',
                 isInEuropeanUnion: bool = False):
        anId = str(uuid4())
        super().__init__(id=anId, type='user')

        self._geoNameId = geoNameId
        self._localeCode = localeCode
        self._continentCode = continentCode
        self._continentName = continentName
        self._countryIsoCode = countryIsoCode
        self._countryName = countryName
        self._isInEuropeanUnion = isInEuropeanUnion

    @classmethod
    def createFrom(self, geoNameId: str = '', localeCode: str = '', continentCode: str = '',
                   continentName: str = '', countryIsoCode: str = '', countryName: str = '',
                   isInEuropeanUnion: bool = False):
        logger.debug(f'[{Country.createFrom.__qualname__}] - with id {id}')
        country = Country(geoNameId=geoNameId, localeCode=localeCode, continentCode=continentCode,
                          continentName=continentName, countryIsoCode=countryIsoCode, countryName=countryName,
                          isInEuropeanUnion=isInEuropeanUnion)
        return country

    def geoNameId(self) -> str:
        return self._geoNameId

    def localeCode(self) -> str:
        return self._localeCode

    def continentCode(self) -> str:
        return self._continentCode

    def continentName(self) -> str:
        return self._continentName

    def countryIsoCode(self) -> str:
        return self._countryIsoCode

    def countryName(self) -> str:
        return self._countryName

    def isInEuropeanUnion(self) -> bool:
        return self._isInEuropeanUnion

    def toMap(self) -> dict:
        return {"geoNameId": self.geoNameId()}

    def __repr__(self):
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __str__(self) -> str:
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __eq__(self, other):
        if not isinstance(other, Country):
            raise NotImplementedError(f'other: {other} can not be compared with Country class')
        return self.geoNameId() == other.geoNameId()
