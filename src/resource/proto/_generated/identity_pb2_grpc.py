# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import identity_pb2 as identity__pb2


class UserAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.userByUsernameAndPassword = channel.unary_unary(
                '/UserAppService/userByUsernameAndPassword',
                request_serializer=identity__pb2.UserAppService_userByUsernameAndPasswordRequest.SerializeToString,
                response_deserializer=identity__pb2.UserAppService_userByUsernameAndPasswordResponse.FromString,
                )


class UserAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def userByUsernameAndPassword(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'userByUsernameAndPassword': grpc.unary_unary_rpc_method_handler(
                    servicer.userByUsernameAndPassword,
                    request_deserializer=identity__pb2.UserAppService_userByUsernameAndPasswordRequest.FromString,
                    response_serializer=identity__pb2.UserAppService_userByUsernameAndPasswordResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'UserAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def userByUsernameAndPassword(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserAppService/userByUsernameAndPassword',
            identity__pb2.UserAppService_userByUsernameAndPasswordRequest.SerializeToString,
            identity__pb2.UserAppService_userByUsernameAndPasswordResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class RoleAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.roleByName = channel.unary_unary(
                '/RoleAppService/roleByName',
                request_serializer=identity__pb2.RoleAppService_roleByNameRequest.SerializeToString,
                response_deserializer=identity__pb2.RoleAppService_roleByNameResponse.FromString,
                )


class RoleAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def roleByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RoleAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'roleByName': grpc.unary_unary_rpc_method_handler(
                    servicer.roleByName,
                    request_deserializer=identity__pb2.RoleAppService_roleByNameRequest.FromString,
                    response_serializer=identity__pb2.RoleAppService_roleByNameResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RoleAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RoleAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def roleByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RoleAppService/roleByName',
            identity__pb2.RoleAppService_roleByNameRequest.SerializeToString,
            identity__pb2.RoleAppService_roleByNameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class PermissionAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.permissionByName = channel.unary_unary(
                '/PermissionAppService/permissionByName',
                request_serializer=identity__pb2.PermissionAppService_permissionByNameRequest.SerializeToString,
                response_deserializer=identity__pb2.PermissionAppService_permissionByNameResponse.FromString,
                )


class PermissionAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def permissionByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PermissionAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'permissionByName': grpc.unary_unary_rpc_method_handler(
                    servicer.permissionByName,
                    request_deserializer=identity__pb2.PermissionAppService_permissionByNameRequest.FromString,
                    response_serializer=identity__pb2.PermissionAppService_permissionByNameResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PermissionAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PermissionAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def permissionByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PermissionAppService/permissionByName',
            identity__pb2.PermissionAppService_permissionByNameRequest.SerializeToString,
            identity__pb2.PermissionAppService_permissionByNameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class OuAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ouByName = channel.unary_unary(
                '/OuAppService/ouByName',
                request_serializer=identity__pb2.OuAppService_ouByNameRequest.SerializeToString,
                response_deserializer=identity__pb2.OuAppService_ouByNameResponse.FromString,
                )


class OuAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ouByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OuAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ouByName': grpc.unary_unary_rpc_method_handler(
                    servicer.ouByName,
                    request_deserializer=identity__pb2.OuAppService_ouByNameRequest.FromString,
                    response_serializer=identity__pb2.OuAppService_ouByNameResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'OuAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OuAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ouByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OuAppService/ouByName',
            identity__pb2.OuAppService_ouByNameRequest.SerializeToString,
            identity__pb2.OuAppService_ouByNameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class RealmAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.realmByName = channel.unary_unary(
                '/RealmAppService/realmByName',
                request_serializer=identity__pb2.RealmAppService_realmByNameRequest.SerializeToString,
                response_deserializer=identity__pb2.RealmAppService_realmByNameResponse.FromString,
                )


class RealmAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def realmByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RealmAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'realmByName': grpc.unary_unary_rpc_method_handler(
                    servicer.realmByName,
                    request_deserializer=identity__pb2.RealmAppService_realmByNameRequest.FromString,
                    response_serializer=identity__pb2.RealmAppService_realmByNameResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RealmAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RealmAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def realmByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RealmAppService/realmByName',
            identity__pb2.RealmAppService_realmByNameRequest.SerializeToString,
            identity__pb2.RealmAppService_realmByNameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ProjectAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.projectByName = channel.unary_unary(
                '/ProjectAppService/projectByName',
                request_serializer=identity__pb2.ProjectAppService_projectByNameRequest.SerializeToString,
                response_deserializer=identity__pb2.ProjectAppService_projectByNameResponse.FromString,
                )


class ProjectAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def projectByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProjectAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'projectByName': grpc.unary_unary_rpc_method_handler(
                    servicer.projectByName,
                    request_deserializer=identity__pb2.ProjectAppService_projectByNameRequest.FromString,
                    response_serializer=identity__pb2.ProjectAppService_projectByNameResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ProjectAppService', rpc_method_handlers)
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
        return grpc.experimental.unary_unary(request, target, '/ProjectAppService/projectByName',
            identity__pb2.ProjectAppService_projectByNameRequest.SerializeToString,
            identity__pb2.ProjectAppService_projectByNameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ResourceTypeAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.resourceTypeByName = channel.unary_unary(
                '/ResourceTypeAppService/resourceTypeByName',
                request_serializer=identity__pb2.ResourceTypeAppService_resourceTypeByNameRequest.SerializeToString,
                response_deserializer=identity__pb2.ResourceTypeAppService_resourceTypeByNameResponse.FromString,
                )


class ResourceTypeAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def resourceTypeByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ResourceTypeAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'resourceTypeByName': grpc.unary_unary_rpc_method_handler(
                    servicer.resourceTypeByName,
                    request_deserializer=identity__pb2.ResourceTypeAppService_resourceTypeByNameRequest.FromString,
                    response_serializer=identity__pb2.ResourceTypeAppService_resourceTypeByNameResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ResourceTypeAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ResourceTypeAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def resourceTypeByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ResourceTypeAppService/resourceTypeByName',
            identity__pb2.ResourceTypeAppService_resourceTypeByNameRequest.SerializeToString,
            identity__pb2.ResourceTypeAppService_resourceTypeByNameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
