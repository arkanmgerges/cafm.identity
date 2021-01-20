# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from identity import city_app_service_pb2 as identity_dot_city__app__service__pb2


class CityAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.cityById = channel.unary_unary(
                '/cafm.identity.country.CityAppService/cityById',
                request_serializer=identity_dot_city__app__service__pb2.CityAppService_cityByIdRequest.SerializeToString,
                response_deserializer=identity_dot_city__app__service__pb2.CityAppService_cityByIdResponse.FromString,
                )
        self.cities = channel.unary_unary(
                '/cafm.identity.country.CityAppService/cities',
                request_serializer=identity_dot_city__app__service__pb2.CityAppService_citiesRequest.SerializeToString,
                response_deserializer=identity_dot_city__app__service__pb2.CityAppService_citiesResponse.FromString,
                )


class CityAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def cityById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def cities(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CityAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'cityById': grpc.unary_unary_rpc_method_handler(
                    servicer.cityById,
                    request_deserializer=identity_dot_city__app__service__pb2.CityAppService_cityByIdRequest.FromString,
                    response_serializer=identity_dot_city__app__service__pb2.CityAppService_cityByIdResponse.SerializeToString,
            ),
            'cities': grpc.unary_unary_rpc_method_handler(
                    servicer.cities,
                    request_deserializer=identity_dot_city__app__service__pb2.CityAppService_citiesRequest.FromString,
                    response_serializer=identity_dot_city__app__service__pb2.CityAppService_citiesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cafm.identity.country.CityAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CityAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def cityById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.country.CityAppService/cityById',
            identity_dot_city__app__service__pb2.CityAppService_cityByIdRequest.SerializeToString,
            identity_dot_city__app__service__pb2.CityAppService_cityByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def cities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.country.CityAppService/cities',
            identity_dot_city__app__service__pb2.CityAppService_citiesRequest.SerializeToString,
            identity_dot_city__app__service__pb2.CityAppService_citiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)