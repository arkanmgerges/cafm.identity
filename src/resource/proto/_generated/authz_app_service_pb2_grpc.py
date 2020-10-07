# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import authz_app_service_pb2 as authz__app__service__pb2


class AuthzAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.isAllowedByToken = channel.unary_unary(
                '/cafm.identity.authz.AuthzAppService/isAllowedByToken',
                request_serializer=authz__app__service__pb2.AuthzAppService_isAllowedRequest.SerializeToString,
                response_deserializer=authz__app__service__pb2.AuthzAppService_isAllowedResponse.FromString,
                )


class AuthzAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def isAllowedByToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthzAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'isAllowedByToken': grpc.unary_unary_rpc_method_handler(
                    servicer.isAllowedByToken,
                    request_deserializer=authz__app__service__pb2.AuthzAppService_isAllowedRequest.FromString,
                    response_serializer=authz__app__service__pb2.AuthzAppService_isAllowedResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cafm.identity.authz.AuthzAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AuthzAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def isAllowedByToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.authz.AuthzAppService/isAllowedByToken',
            authz__app__service__pb2.AuthzAppService_isAllowedRequest.SerializeToString,
            authz__app__service__pb2.AuthzAppService_isAllowedResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
