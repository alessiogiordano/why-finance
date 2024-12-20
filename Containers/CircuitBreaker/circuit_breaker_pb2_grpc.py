# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import circuit_breaker_pb2 as circuit__breaker__pb2


class CircuitBreakerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.status = channel.unary_unary(
                '/CircuitBreaker/status',
                request_serializer=circuit__breaker__pb2.CircuitBreakerStatusRequest.SerializeToString,
                response_deserializer=circuit__breaker__pb2.CircuitBreakerStatusResponse.FromString,
                )
        self.success = channel.unary_unary(
                '/CircuitBreaker/success',
                request_serializer=circuit__breaker__pb2.CircuitBreakerStatusRequest.SerializeToString,
                response_deserializer=circuit__breaker__pb2.CircuitBreakerStatusResponse.FromString,
                )
        self.failure = channel.unary_unary(
                '/CircuitBreaker/failure',
                request_serializer=circuit__breaker__pb2.CircuitBreakerStatusRequest.SerializeToString,
                response_deserializer=circuit__breaker__pb2.CircuitBreakerStatusResponse.FromString,
                )
        self.send = channel.unary_unary(
                '/CircuitBreaker/send',
                request_serializer=circuit__breaker__pb2.CircuitBreakerHTTPRequest.SerializeToString,
                response_deserializer=circuit__breaker__pb2.CircuitBreakerHTTPResponse.FromString,
                )


class CircuitBreakerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def status(self, request, context):
        """Manual get/set
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def success(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def failure(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def send(self, request, context):
        """Delegated HTTP client
        TODO: Get state of "service_id" i.e. host
        TODO: Report success/failure on "service_id"
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CircuitBreakerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'status': grpc.unary_unary_rpc_method_handler(
                    servicer.status,
                    request_deserializer=circuit__breaker__pb2.CircuitBreakerStatusRequest.FromString,
                    response_serializer=circuit__breaker__pb2.CircuitBreakerStatusResponse.SerializeToString,
            ),
            'success': grpc.unary_unary_rpc_method_handler(
                    servicer.success,
                    request_deserializer=circuit__breaker__pb2.CircuitBreakerStatusRequest.FromString,
                    response_serializer=circuit__breaker__pb2.CircuitBreakerStatusResponse.SerializeToString,
            ),
            'failure': grpc.unary_unary_rpc_method_handler(
                    servicer.failure,
                    request_deserializer=circuit__breaker__pb2.CircuitBreakerStatusRequest.FromString,
                    response_serializer=circuit__breaker__pb2.CircuitBreakerStatusResponse.SerializeToString,
            ),
            'send': grpc.unary_unary_rpc_method_handler(
                    servicer.send,
                    request_deserializer=circuit__breaker__pb2.CircuitBreakerHTTPRequest.FromString,
                    response_serializer=circuit__breaker__pb2.CircuitBreakerHTTPResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CircuitBreaker', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CircuitBreaker(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CircuitBreaker/status',
            circuit__breaker__pb2.CircuitBreakerStatusRequest.SerializeToString,
            circuit__breaker__pb2.CircuitBreakerStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def success(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CircuitBreaker/success',
            circuit__breaker__pb2.CircuitBreakerStatusRequest.SerializeToString,
            circuit__breaker__pb2.CircuitBreakerStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def failure(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CircuitBreaker/failure',
            circuit__breaker__pb2.CircuitBreakerStatusRequest.SerializeToString,
            circuit__breaker__pb2.CircuitBreakerStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def send(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CircuitBreaker/send',
            circuit__breaker__pb2.CircuitBreakerHTTPRequest.SerializeToString,
            circuit__breaker__pb2.CircuitBreakerHTTPResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
