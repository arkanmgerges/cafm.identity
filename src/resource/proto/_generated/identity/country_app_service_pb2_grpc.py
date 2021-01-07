# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from identity import country_app_service_pb2 as identity_dot_country__app__service__pb2


class CountryAppServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.countryById = channel.unary_unary(
                '/cafm.identity.country.CountryAppService/countryById',
                request_serializer=identity_dot_country__app__service__pb2.CountryAppService_countryByIdRequest.SerializeToString,
                response_deserializer=identity_dot_country__app__service__pb2.CountryAppService_countryByIdResponse.FromString,
                )
        self.countries = channel.unary_unary(
                '/cafm.identity.country.CountryAppService/countries',
                request_serializer=identity_dot_country__app__service__pb2.CountryAppService_countriesRequest.SerializeToString,
                response_deserializer=identity_dot_country__app__service__pb2.CountryAppService_countriesResponse.FromString,
                )
        self.countryCities = channel.unary_unary(
                '/cafm.identity.country.CountryAppService/countryCities',
                request_serializer=identity_dot_country__app__service__pb2.CountryAppService_countryCitiesRequest.SerializeToString,
                response_deserializer=identity_dot_country__app__service__pb2.CountryAppService_countryCitiesResponse.FromString,
                )
        self.countryCity = channel.unary_unary(
                '/cafm.identity.country.CountryAppService/countryCity',
                request_serializer=identity_dot_country__app__service__pb2.CountryAppService_countryCityRequest.SerializeToString,
                response_deserializer=identity_dot_country__app__service__pb2.CountryAppService_countryCityResponse.FromString,
                )


class CountryAppServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def countryById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def countries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def countryCities(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def countryCity(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CountryAppServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'countryById': grpc.unary_unary_rpc_method_handler(
                    servicer.countryById,
                    request_deserializer=identity_dot_country__app__service__pb2.CountryAppService_countryByIdRequest.FromString,
                    response_serializer=identity_dot_country__app__service__pb2.CountryAppService_countryByIdResponse.SerializeToString,
            ),
            'countries': grpc.unary_unary_rpc_method_handler(
                    servicer.countries,
                    request_deserializer=identity_dot_country__app__service__pb2.CountryAppService_countriesRequest.FromString,
                    response_serializer=identity_dot_country__app__service__pb2.CountryAppService_countriesResponse.SerializeToString,
            ),
            'countryCities': grpc.unary_unary_rpc_method_handler(
                    servicer.countryCities,
                    request_deserializer=identity_dot_country__app__service__pb2.CountryAppService_countryCitiesRequest.FromString,
                    response_serializer=identity_dot_country__app__service__pb2.CountryAppService_countryCitiesResponse.SerializeToString,
            ),
            'countryCity': grpc.unary_unary_rpc_method_handler(
                    servicer.countryCity,
                    request_deserializer=identity_dot_country__app__service__pb2.CountryAppService_countryCityRequest.FromString,
                    response_serializer=identity_dot_country__app__service__pb2.CountryAppService_countryCityResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cafm.identity.country.CountryAppService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CountryAppService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def countryById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.country.CountryAppService/countryById',
            identity_dot_country__app__service__pb2.CountryAppService_countryByIdRequest.SerializeToString,
            identity_dot_country__app__service__pb2.CountryAppService_countryByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def countries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.country.CountryAppService/countries',
            identity_dot_country__app__service__pb2.CountryAppService_countriesRequest.SerializeToString,
            identity_dot_country__app__service__pb2.CountryAppService_countriesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def countryCities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.country.CountryAppService/countryCities',
            identity_dot_country__app__service__pb2.CountryAppService_countryCitiesRequest.SerializeToString,
            identity_dot_country__app__service__pb2.CountryAppService_countryCitiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def countryCity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cafm.identity.country.CountryAppService/countryCity',
            identity_dot_country__app__service__pb2.CountryAppService_countryCityRequest.SerializeToString,
            identity_dot_country__app__service__pb2.CountryAppService_countryCityResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
