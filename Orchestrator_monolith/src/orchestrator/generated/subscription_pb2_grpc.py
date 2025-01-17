# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import subscription_pb2 as subscription__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in subscription_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class SubscriptionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateSubscription = channel.unary_unary(
                '/subscription.SubscriptionService/CreateSubscription',
                request_serializer=subscription__pb2.CreateSubscriptionRequest.SerializeToString,
                response_deserializer=subscription__pb2.CreateSubscriptionResponse.FromString,
                _registered_method=True)
        self.GetSubscriptions = channel.unary_unary(
                '/subscription.SubscriptionService/GetSubscriptions',
                request_serializer=subscription__pb2.GetSubscriptionsRequest.SerializeToString,
                response_deserializer=subscription__pb2.GetSubscriptionsResponse.FromString,
                _registered_method=True)
        self.ChangeSubscription = channel.unary_unary(
                '/subscription.SubscriptionService/ChangeSubscription',
                request_serializer=subscription__pb2.ChangeSubscriptionRequest.SerializeToString,
                response_deserializer=subscription__pb2.ChangeSubscriptionResponse.FromString,
                _registered_method=True)
        self.OptOutPolicy = channel.unary_unary(
                '/subscription.SubscriptionService/OptOutPolicy',
                request_serializer=subscription__pb2.OptOutPolicyRequest.SerializeToString,
                response_deserializer=subscription__pb2.OptOutPolicyResponse.FromString,
                _registered_method=True)
        self.DeleteSubscription = channel.unary_unary(
                '/subscription.SubscriptionService/DeleteSubscription',
                request_serializer=subscription__pb2.DeleteSubscriptionRequest.SerializeToString,
                response_deserializer=subscription__pb2.DeleteSubscriptionResponse.FromString,
                _registered_method=True)
        self.ActivateSubscription = channel.unary_unary(
                '/subscription.SubscriptionService/ActivateSubscription',
                request_serializer=subscription__pb2.ActivateSubscriptionRequest.SerializeToString,
                response_deserializer=subscription__pb2.ActivateSubscriptionResponse.FromString,
                _registered_method=True)
        self.DeactivateSubscription = channel.unary_unary(
                '/subscription.SubscriptionService/DeactivateSubscription',
                request_serializer=subscription__pb2.DeactivateSubscriptionRequest.SerializeToString,
                response_deserializer=subscription__pb2.DeactivateSubscriptionResponse.FromString,
                _registered_method=True)
        self.GetSubscriptionsDynamoDB = channel.unary_unary(
                '/subscription.SubscriptionService/GetSubscriptionsDynamoDB',
                request_serializer=subscription__pb2.GetSubscriptionsDynamoDBRequest.SerializeToString,
                response_deserializer=subscription__pb2.GetSubscriptionsDynamoDBResponse.FromString,
                _registered_method=True)


class SubscriptionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateSubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSubscriptions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChangeSubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OptOutPolicy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteSubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ActivateSubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeactivateSubscription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSubscriptionsDynamoDB(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SubscriptionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateSubscription,
                    request_deserializer=subscription__pb2.CreateSubscriptionRequest.FromString,
                    response_serializer=subscription__pb2.CreateSubscriptionResponse.SerializeToString,
            ),
            'GetSubscriptions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSubscriptions,
                    request_deserializer=subscription__pb2.GetSubscriptionsRequest.FromString,
                    response_serializer=subscription__pb2.GetSubscriptionsResponse.SerializeToString,
            ),
            'ChangeSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.ChangeSubscription,
                    request_deserializer=subscription__pb2.ChangeSubscriptionRequest.FromString,
                    response_serializer=subscription__pb2.ChangeSubscriptionResponse.SerializeToString,
            ),
            'OptOutPolicy': grpc.unary_unary_rpc_method_handler(
                    servicer.OptOutPolicy,
                    request_deserializer=subscription__pb2.OptOutPolicyRequest.FromString,
                    response_serializer=subscription__pb2.OptOutPolicyResponse.SerializeToString,
            ),
            'DeleteSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteSubscription,
                    request_deserializer=subscription__pb2.DeleteSubscriptionRequest.FromString,
                    response_serializer=subscription__pb2.DeleteSubscriptionResponse.SerializeToString,
            ),
            'ActivateSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.ActivateSubscription,
                    request_deserializer=subscription__pb2.ActivateSubscriptionRequest.FromString,
                    response_serializer=subscription__pb2.ActivateSubscriptionResponse.SerializeToString,
            ),
            'DeactivateSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.DeactivateSubscription,
                    request_deserializer=subscription__pb2.DeactivateSubscriptionRequest.FromString,
                    response_serializer=subscription__pb2.DeactivateSubscriptionResponse.SerializeToString,
            ),
            'GetSubscriptionsDynamoDB': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSubscriptionsDynamoDB,
                    request_deserializer=subscription__pb2.GetSubscriptionsDynamoDBRequest.FromString,
                    response_serializer=subscription__pb2.GetSubscriptionsDynamoDBResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'subscription.SubscriptionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('subscription.SubscriptionService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class SubscriptionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/subscription.SubscriptionService/CreateSubscription',
            subscription__pb2.CreateSubscriptionRequest.SerializeToString,
            subscription__pb2.CreateSubscriptionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetSubscriptions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/subscription.SubscriptionService/GetSubscriptions',
            subscription__pb2.GetSubscriptionsRequest.SerializeToString,
            subscription__pb2.GetSubscriptionsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ChangeSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/subscription.SubscriptionService/ChangeSubscription',
            subscription__pb2.ChangeSubscriptionRequest.SerializeToString,
            subscription__pb2.ChangeSubscriptionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def OptOutPolicy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/subscription.SubscriptionService/OptOutPolicy',
            subscription__pb2.OptOutPolicyRequest.SerializeToString,
            subscription__pb2.OptOutPolicyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/subscription.SubscriptionService/DeleteSubscription',
            subscription__pb2.DeleteSubscriptionRequest.SerializeToString,
            subscription__pb2.DeleteSubscriptionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ActivateSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/subscription.SubscriptionService/ActivateSubscription',
            subscription__pb2.ActivateSubscriptionRequest.SerializeToString,
            subscription__pb2.ActivateSubscriptionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeactivateSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/subscription.SubscriptionService/DeactivateSubscription',
            subscription__pb2.DeactivateSubscriptionRequest.SerializeToString,
            subscription__pb2.DeactivateSubscriptionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetSubscriptionsDynamoDB(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/subscription.SubscriptionService/GetSubscriptionsDynamoDB',
            subscription__pb2.GetSubscriptionsDynamoDBRequest.SerializeToString,
            subscription__pb2.GetSubscriptionsDynamoDBResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
