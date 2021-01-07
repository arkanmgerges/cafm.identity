"""
    @author: Mohammad S. moso<moso@develoop.run>
"""

from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.resource.logging.logger import logger


class City(Resource):
    def __init__(self, id: str = None, geoNameId: str = '', localeCode: str = '', continentCode: str = '',
                 continentName: str = '', countryIsoCode: str = '', countryName: str = '',
                 subdivisionOneIsoCode: str = '', subdivisionOneIsoName: str = '', subdivisionTwoIsoCode: str = '',
                 subdivisionTwoIsoName: str = '', cityName: str = '', metroCode: str = '', timeZone: str = '',
                 isInEuropeanUnion: bool = False):
        anId = str(uuid4()) if id is None or id == '' else id
        super().__init__(id=anId)

        self._geoNameId = geoNameId
        self._localeCode = localeCode
        self._continentCode = continentCode
        self._continentName = continentName
        self._countryIsoCode = countryIsoCode
        self._countryName = countryName
        self._subdivisionOneIsoCode = subdivisionOneIsoCode
        self._subdivisionOneIsoName = subdivisionOneIsoName
        self._subdivisionTwoIsoCode = subdivisionTwoIsoCode
        self._subdivisionTwoIsoName = subdivisionTwoIsoName
        self._cityName = cityName
        self._metroCode = metroCode
        self._timeZone = timeZone
        self._isInEuropeanUnion = isInEuropeanUnion

    @classmethod
    def createFrom(self, id: str = None, geoNameId: str = '', localeCode: str = '', continentCode: str = '',
                   continentName: str = '', countryIsoCode: str = '', countryName: str = '',
                   subdivisionOneIsoCode: str = '', subdivisionOneIsoName: str = '', subdivisionTwoIsoCode: str = '',
                   subdivisionTwoIsoName: str = '', cityName: str = '', metroCode: str = '', timeZone: str = '',
                   isInEuropeanUnion: bool = False):
        logger.debug(f'[{City.createFrom.__qualname__}] - with id {id}')

        city = City(id=id, geoNameId=geoNameId, localeCode=localeCode, continentCode=continentCode,
                    continentName=continentName, countryIsoCode=countryIsoCode, countryName=countryName,
                    subdivisionOneIsoCode=subdivisionOneIsoCode, subdivisionOneIsoName=subdivisionOneIsoName,
                    subdivisionTwoIsoCode=subdivisionTwoIsoCode, subdivisionTwoIsoName=subdivisionTwoIsoName,
                    cityName=cityName, metroCode=metroCode, timeZone=timeZone, isInEuropeanUnion=isInEuropeanUnion)
        return city

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

    def subdivisionOneIsoCode(self) -> str:
        return self._subdivisionOneIsoCode

    def subdivisionOneIsoName(self) -> str:
        return self._subdivisionOneIsoName

    def subdivisionTwoIsoCode(self) -> str:
        return self._subdivisionTwoIsoCode

    def subdivisionTwoIsoName(self) -> str:
        return self._subdivisionTwoIsoName

    def cityName(self) -> str:
        return self._cityName

    def metroCode(self) -> str:
        return self._metroCode

    def timeZone(self) -> str:
        return self._timeZone

    def isInEuropeanUnion(self) -> bool:
        return self._isInEuropeanUnion

    def toMap(self) -> dict:
        return {"id": self.id()}

    def __repr__(self):
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __str__(self) -> str:
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __eq__(self, other):
        if not isinstance(other, City):
            raise NotImplementedError(f'other: {other} can not be compared with City class')
        return self.id() == other.id()
