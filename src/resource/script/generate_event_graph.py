"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>

After you run this script, it will generate to formats in the folder specified below in `OUTPUT_FILE_NAME`

In order to generate svg using dot format
cat src/resource/graph_data/graph.dot | docker run --rm -i nshine/dot:2.40.1 dot -Tsvg > src/resource/graph_data/graph.svg

In order to generate svg or pdf using mermaid format
docker run -v $(pwd):/app minlag/mermaid-cli:8.8.4-1 -i /app/src/resource/graph_data/graph.mmd -o /app/src/resource/graph_data/graph.pdf
"""
import glob
import os
import re

OUTPUT_FILE_NAME = f'{os.path.dirname(os.path.abspath(__file__))}/../graph_data/graph'

# key, val, command to command, and event to command
idConnections = {}
# cmd and events
typeDef = {}

currentGroupName = 'identity'

cmd1Reg = re.compile(r'CommonCommandConstant.(?P<itemCapturedName>\w+)')
cmd2Reg = re.compile(r'CommonCommandConstant.(?P<itemCapturedName>\w+)\.')
evtReg = re.compile(r'CommonEventConstant.(?P<itemCapturedName>\w+)')
cmdWithTypeReg = re.compile(r'/(?P<groupName>\w+)_(?P<groupType>\w+)/handler')

files = list(filter(lambda x: x.find('__init__.py') == -1,
                    glob.glob(
                        f'{os.path.dirname(os.path.abspath(__file__))}\
/../../../src/port_adapter/messaging/listener/**/handler/**/*.py')))

handlers = list(
    map(lambda x: x.strip('.py'),
        list(map(lambda x: x[x.find('src.port_adapter.messaging'):],
                 map(lambda x: x.replace('/', '.'),
                     files)))))


def readFile(filePath: str) -> str:
    with open(filePath) as f:
        data = f.read()
        return data


def extractData():
    for filePath in files:
        data = readFile(filePath)
        r = cmdWithTypeReg.search(filePath)
        groupName = r.group('groupName')
        groupType = r.group('groupType')
        if groupType == 'command':
            cmd = extractFirstCommand(data=data)
            saveCommand(cmdWord=cmd, groupName=groupName, groupType=groupType)
        if groupType == 'event':
            event = extractEvent(data=data)
            saveEvent(eventWord=event, groupName=groupName, groupType=groupType)

        extractConnection(data=data, groupName=groupName, groupType=groupType)


def extractEvent(data: str) -> str:
    """
    Add the event word (e.g. UserCreated) into the key of the group name (e.g. api, identity, ...etc)
    """
    r = evtReg.search(data)
    eventWord = None
    if r is not None:
        eventWord = r.group('itemCapturedName')
    return eventWord


def extractConnection(data: str, groupName: str, groupType: str):
    if groupName == 'api' and groupType == 'command':
        cmd1 = extractFirstCommand(data=data)
        cmd2 = extractSecondCommand(data=data)
        if cmd1 is None and cmd2 is not None:
            cmd1 = cmd2
        if cmd2 is None and cmd1 is not None:
            cmd2 = cmd1
        if cmd1 is not None and cmd2 is not None:
            idConnections[constructId(groupName=groupName, word=cmd1, groupType=groupType)] = \
                constructId(groupName=currentGroupName, word=cmd2, groupType='command')
    elif groupType == 'event':
        evt = extractEvent(data=data)
        cmd = extractSecondCommand(data=data)
        if cmd is None:
            cmd = extractFirstCommand(data=data)
        idConnections[constructId(groupName=groupName, word=evt, groupType=groupType)] = \
            constructId(groupName=currentGroupName, word=cmd, groupType='command')


def extractFirstCommand(data: str, ) -> str:
    """
    Add the command word (e.g. CreateUser) into the key of the group name (e.g. api, identity, ...etc)
    """
    r = cmd1Reg.search(data)
    cmdWord = None
    if r is not None:
        cmdWord = r.group('itemCapturedName')
    return cmdWord


def extractSecondCommand(data: str) -> str:
    """
    Add the command word (e.g. CreateUser) into the key of the group name (e.g. api, identity, ...etc)
    """
    r = cmd2Reg.search(data)
    cmdWord = None
    if r is not None:
        cmdWord = r.group('itemCapturedName')
    return cmdWord


def saveCommand(cmdWord: str, groupName: str, groupType: str):
    if groupName not in typeDef:
        typeDef[groupName] = {}
    typeDef[groupName][constructId(groupName=groupName, word=cmdWord, groupType=groupType)] = cmdWord


def saveEvent(eventWord: str, groupName: str, groupType: str):
    if groupName not in typeDef:
        typeDef[groupName] = {}
    typeDef[groupName][constructId(groupName=groupName, word=eventWord, groupType=groupType)] = eventWord


def constructId(groupName: str, word: str, groupType: str):
    """
    Construct an id to be used as a key into the dictionary
    """
    return f'{groupName}{groupType.capitalize()}Id{word}'


def saveToMermaidFile():
    resultSt = '''graph LR
classDef eventCls fill:orange;
classDef commandCls fill:lightBlue;
    '''
    resultList = []
    for key in typeDef.keys():
        resultSt += f"\nsubgraph {key.capitalize()}\n"
        for key2, value2 in typeDef[key].items():
            st = f'\t{key2}[{value2}]'
            st += ':::commandCls' if 'Command' in key2 else ':::eventCls'
            resultList.append(st)

        resultSt += '\n'.join(resultList)
        resultSt += "\nend\n"
        resultList = []

    # Add connections
    resultSt += '\n'
    for key, value in idConnections.items():
        st = f'{key}-->{value}'
        resultList.append(st)
    resultSt += '\n'.join(resultList)

    with open(f'{OUTPUT_FILE_NAME}.mmd', 'w') as f:
        f.write(resultSt)


def saveToDotFile():
    resultSt = 'digraph G {\n'
    resultList = []
    clusterCounter = 0
    for key in typeDef.keys():
        resultSt += f"\nsubgraph cluster{clusterCounter} {{\n\tlabel=\"{key.capitalize()}\";\n\tstyle=filled;\n" \
                    f"\tcolor=lightgrey;\n\tnode [shape=box,style=filled];\n"
        clusterCounter += 1
        for key2, value2 in typeDef[key].items():
            color = 'lightBlue' if 'Command' in key2 else 'orange'
            st = f'\t{key2} [label={value2}, color={color}];\n'
            st += f'\t{key2};'
            resultList.append(st)

        resultSt += '\n'.join(resultList)
        resultSt += "\n}\n"
        resultList = []

    # Add connections
    resultSt += '\n'
    for key, value in idConnections.items():
        st = f'{key}->{value};'
        resultList.append(st)
    resultSt += '\n'.join(resultList)

    resultSt += '\n}'
    with open(f'{OUTPUT_FILE_NAME}.dot', 'w') as f:
        f.write(resultSt)


extractData()
saveToMermaidFile()
saveToDotFile()
