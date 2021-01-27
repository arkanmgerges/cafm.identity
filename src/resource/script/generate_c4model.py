"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import glob
import os
import re
from typing import List

OUTPUT_FILE_NAME = f'{os.path.dirname(os.path.abspath(__file__))}/../graph_data/graph_c4model'

outsideResult = set()
insideResult = {}

inside = re.compile(r'c4model\|cb\|(?P<microservice>\w+):(?P<item>[^\n]+)')
outside = re.compile(r'c4model:(?P<item>[^\n]+)')

files = []
for filePath in ['/Users/arkan/dev/company/digital-mob/cafm/cafm-api/**/*.py',
                 '/Users/arkan/dev/company/digital-mob/cafm/cafm-identity/**/*.py',
                 '/Users/arkan/dev/company/digital-mob/cafm/cafm-project/**/*.py']:
    files.extend(list(filter(lambda x: x.find('__init__.py') == -1 and
                                       x.find('src/resource') == -1 and
                                       x.find('cafm-identity/test') == -1 and
                                       x.find('cafm-identity/doc') == -1,
                             glob.glob(filePath, recursive=True))))


def extractData():
    for filePath in files:
        data = readFile(filePath)
        outResult = outside.findall(data)
        if len(outResult) > 0:
            _addToOutside(outResult=outResult)
        inResult = inside.findall(data)
        if len(inResult) > 0:
            _addToInside(inResult=inResult)


def _addToOutside(outResult: List):
    for x in outResult:
        outsideResult.add(x)


def _addToInside(inResult: List):
    for x in inResult:
        if x[0] != '':
            if x[0] not in insideResult:
                insideResult[x[0]] = set()
            insideResult[x[0]].add(x[1])


def readFile(filePath: str) -> str:
    with open(filePath) as f:
        data = f.read()
        return data


def saveToPumlFile():
    resultSt = '''@startuml "system_c4model"
!include puml/c4_container.puml
!include puml/c4_component.puml

skinparam wrapWidth 200
skinparam maxMessageSize 200

LAYOUT_TOP_DOWN()
'LAYOUT_AS_SKETCH()
LAYOUT_WITH_LEGEND()\n

Container_Boundary(redis, "Redis System") {
	Component(api__redis, "Api Caching & Response", "tcp", "Has response, caching results")
}
'''

    # Container boundry
    for microservice, itemList in insideResult.items():
        if microservice == 'api':
            resultSt += 'Container_Boundary(api, "Api Microservice") {\n'
            for item in itemList:
                resultSt += f'\t{item}\n'
            resultSt += '}\n'

        if microservice == 'identity':
            resultSt += 'Container_Boundary(identity, "Identity Microservice") {\n'
            for item in itemList:
                resultSt += f'\t{item}\n'
            resultSt += '}\n'

        if microservice == 'project':
            resultSt += 'Container_Boundary(project, "Project Microservice") {\n'
            for item in itemList:
                resultSt += f'\t{item}\n'
            resultSt += '}\n'

    # Global
    for item in outsideResult:
        resultSt += f'{item}\n'

    resultSt += 'Rel(api, redis, "Get/Create api response & caching data")\n'
    resultSt += '\n@enduml\n'

    with open(f'{OUTPUT_FILE_NAME}.puml', 'w') as f:
        f.write(resultSt)


extractData()
saveToPumlFile()
