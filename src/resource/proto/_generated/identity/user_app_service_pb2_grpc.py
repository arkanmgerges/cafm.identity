# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from identity import user_app_service_pb2 as identity_dot_user__app__service__pb2


class UserAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.userByEmailAndPassword = channel.unary_unary(
                '/cafm.identity.user.UserAppService/userByEmailAndPassword',
                request_serializer=identity_dot_user__app__service__pb2.UserAppService_userByEmailAndPasswordRequest.SerializeToString,
                response_deserializer=identity_dot_user__app__service__pb2.UserAppService_userByEmailAndPasswordResponse.FromString,
                )
        self.userById = channel.unary_unary(
                '/cafm.identity.user.UserAppService/userById',
                request_serializer=identity_dot_user__app__service__pb2.UserAppService_userByIdRequest.SerializeToString,
                response_deserializer=identity_dot_user__app__service__pb2.UserAppService_userByIdResponse.FromString,
                )
        self.users = channel.unary_unary(
                '/cafm.identity.user.UserAppService/users',
                request_serializer=identity_dot_user__app__service__pb2.UserAppService_usersRequest.SerializeToString,
                response_deserializer=identity_dot_user__app__service__pb2.UserAppService_usersResponse.FromString,
                )
        self.newId = channel.unary_unary(
                '/cafm.identity.user.UserAppService/newId',
                request_serializer=identity_dot_user__app__service__pb2.UserAppService_newIdRequest.SerializeToString,
                response_deserializer=identity_dot_user__app__service__pb2.UserAppService_newIdResponse.FromString,
                )


class UserAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def userByEmailAndPassword(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def userById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def users(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def newId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'userByEmailAndPassword': grpc.unary_unary_rpc_method_handler(
                    servicer.userByEmailAndPassword,
                    request_deserializer=identity_dot_user__app__service__pb2.UserAppService_userByEmailAndPasswordRequest.FromString,
                    response_serializer=identity_dot_user__app__service__pb2.UserAppService_userByEmailAndPasswordResponse.SerializeToString,
            ),
            'userById': grpc.unary_unary_rpc_method_handler(
                    servicer.userById,
                    request_deserializer=identity_dot_user__app__service__pb2.UserAppService_userByIdRequest.FromString,
                    response_serializer=identity_dot_user__app__service__pb2.UserAppService_userByIdResponse.SerializeToString,
            ),
            'users': grpc.unary_unary_rpc_method_handler(
                    servicer.users,
                    request_deserializer=identity_dot_user__app__service__pb2.UserAppService_usersRequest.FromString,
                    response_serializer=identity_dot_user__app__service__pb2.UserAppService_usersResponse.SerializeToString,
            ),
            'newId': grpc.unary_unary_rpc_method_handler(
                    servicer.newId,
                    request_deserializer=identity_dot_user__app__service__pb2.UserAppService_newIdRequest.FromString,
                    response_serializer=identity_dot_user__app__service__pb2.UserAppService_newIdResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cafm.identity.user.UserAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def userByEmailAndPassword(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.user.UserAppService/userByEmailAndPassword',
            identity_dot_user__app__service__pb2.UserAppService_userByEmailAndPasswordRequest.SerializeToString,
            identity_dot_user__app__service__pb2.UserAppService_userByEmailAndPasswordResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def userById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.user.UserAppService/userById',
            identity_dot_user__app__service__pb2.UserAppService_userByIdRequest.SerializeToString,
            identity_dot_user__app__service__pb2.UserAppService_userByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def users(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.user.UserAppService/users',
            identity_dot_user__app__service__pb2.UserAppService_usersRequest.SerializeToString,
            identity_dot_user__app__service__pb2.UserAppService_usersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def newId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.user.UserAppService/newId',
            identity_dot_user__app__service__pb2.UserAppService_newIdRequest.SerializeToString,
            identity_dot_user__app__service__pb2.UserAppService_newIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
