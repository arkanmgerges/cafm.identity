"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

class RequestCheckData:
    def __init__(self, requestId, checkForId=False, resultIdName=None, ignoreIfExists=False, returnResult=True):
        self.requestId = requestId
        self.checkForId=checkForId
        self.resultIdName=resultIdName
        self.ignoreIfExists=ignoreIfExists
        self.returnResult=returnResult