"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.portadapter.AppDi as AppDi
import src.resource.proto._generated.identity_pb2 as identity_pb2
import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.application.RealmApplicationService import RealmApplicationService
from src.domainmodel.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
from src.domainmodel.realm.Realm import Realm


class RealmAppServiceListener(identity_pb2_grpc.RealmAppServiceServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def realmByName(self, request, context):
        try:
            realmAppService: RealmApplicationService = AppDi.instance.get(RealmApplicationService)
            realm: Realm = realmAppService.realmByName(name=request.name)
            return identity_pb2.RealmAppService_realmByNameResponse(id=realm.id(), name=realm.name())
        except RealmDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Realm does not exist')
            return identity_pb2.RealmAppService_realmByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.RealmResponse()
