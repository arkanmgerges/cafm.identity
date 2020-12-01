"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.RealmApplicationService import RealmApplicationService
from src.domain_model.realm.Realm import Realm
from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.proto._generated.realm_app_service_pb2 import RealmAppService_realmByNameResponse, \
    RealmAppService_realmsResponse, RealmAppService_realmByIdResponse
from src.resource.proto._generated.realm_app_service_pb2_grpc import RealmAppServiceServicer


class RealmAppServiceListener(RealmAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    def realmByName(self, request, context):
        try:
            token = self._token(context)
            realmAppService: RealmApplicationService = AppDi.instance.get(RealmApplicationService)
            realm: Realm = realmAppService.realmByName(name=request.name, token=token)
            response = RealmAppService_realmByNameResponse()
            response.realm.id = realm.id()
            response.realm.name = realm.name()
            return response
        except RealmDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Realm does not exist')
            return RealmAppService_realmByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return RealmAppService_realmByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.RealmResponse()

    @debugLogger
    def realms(self, request, context):
        try:
            token = self._token(context)
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            logger.debug(
                f'[{RealmAppServiceListener.realms.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}, token: {token}')
            realmAppService: RealmApplicationService = AppDi.instance.get(RealmApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = realmAppService.realms(
                                                  resultFrom=request.resultFrom,
                                                  resultSize=resultSize,
                                                  token=token,
                                                  order=orderData)
            response = RealmAppService_realmsResponse()
            for realm in result['items']:
                response.realms.add(id=realm.id(), name=realm.name())
            response.itemCount = result['itemCount']
            logger.debug(f'[{RealmAppServiceListener.realms.__qualname__}] - response: {response}')
            return RealmAppService_realmsResponse(realms=response.realms, itemCount=response.itemCount)
        except RealmDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No realms found')
            return RealmAppService_realmByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return RealmAppService_realmByNameResponse()

    @debugLogger
    def realmById(self, request, context):
        try:
            token = self._token(context)
            realmAppService: RealmApplicationService = AppDi.instance.get(RealmApplicationService)
            realm: Realm = realmAppService.realmById(id=request.id, token=token)
            logger.debug(f'[{RealmAppServiceListener.realmById.__qualname__}] - response: {realm}')
            response = RealmAppService_realmByIdResponse()
            response.realm.id = realm.id()
            response.realm.name = realm.name()
            return response
        except RealmDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Realm does not exist')
            return RealmAppService_realmByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return RealmAppService_realmByIdResponse()

    @debugLogger
    def _token(self, context) -> str:
        metadata = context.invocation_metadata()
        if 'token' in metadata[0]:
            return metadata[0].value
        return ''
