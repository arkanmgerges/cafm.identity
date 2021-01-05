# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from identity import project_app_service_pb2 as identity_dot_project__app__service__pb2


class ProjectAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.projectByName = channel.unary_unary(
                '/cafm.identity.project.ProjectAppService/projectByName',
                request_serializer=identity_dot_project__app__service__pb2.ProjectAppService_projectByNameRequest.SerializeToString,
                response_deserializer=identity_dot_project__app__service__pb2.ProjectAppService_projectByNameResponse.FromString,
                )
        self.projectById = channel.unary_unary(
                '/cafm.identity.project.ProjectAppService/projectById',
                request_serializer=identity_dot_project__app__service__pb2.ProjectAppService_projectByIdRequest.SerializeToString,
                response_deserializer=identity_dot_project__app__service__pb2.ProjectAppService_projectByIdResponse.FromString,
                )
        self.projects = channel.unary_unary(
                '/cafm.identity.project.ProjectAppService/projects',
                request_serializer=identity_dot_project__app__service__pb2.ProjectAppService_projectsRequest.SerializeToString,
                response_deserializer=identity_dot_project__app__service__pb2.ProjectAppService_projectsResponse.FromString,
                )


class ProjectAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def projectByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def projectById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def projects(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProjectAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'projectByName': grpc.unary_unary_rpc_method_handler(
                    servicer.projectByName,
                    request_deserializer=identity_dot_project__app__service__pb2.ProjectAppService_projectByNameRequest.FromString,
                    response_serializer=identity_dot_project__app__service__pb2.ProjectAppService_projectByNameResponse.SerializeToString,
            ),
            'projectById': grpc.unary_unary_rpc_method_handler(
                    servicer.projectById,
                    request_deserializer=identity_dot_project__app__service__pb2.ProjectAppService_projectByIdRequest.FromString,
                    response_serializer=identity_dot_project__app__service__pb2.ProjectAppService_projectByIdResponse.SerializeToString,
            ),
            'projects': grpc.unary_unary_rpc_method_handler(
                    servicer.projects,
                    request_deserializer=identity_dot_project__app__service__pb2.ProjectAppService_projectsRequest.FromString,
                    response_serializer=identity_dot_project__app__service__pb2.ProjectAppService_projectsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cafm.identity.project.ProjectAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ProjectAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def projectByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.project.ProjectAppService/projectByName',
            identity_dot_project__app__service__pb2.ProjectAppService_projectByNameRequest.SerializeToString,
            identity_dot_project__app__service__pb2.ProjectAppService_projectByNameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def projectById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.project.ProjectAppService/projectById',
            identity_dot_project__app__service__pb2.ProjectAppService_projectByIdRequest.SerializeToString,
            identity_dot_project__app__service__pb2.ProjectAppService_projectByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def projects(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.project.ProjectAppService/projects',
            identity_dot_project__app__service__pb2.ProjectAppService_projectsRequest.SerializeToString,
            identity_dot_project__app__service__pb2.ProjectAppService_projectsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)