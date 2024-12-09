import grpc
from grpc import ServicerContext
from db.db import USER_DB, SUBSCRIPTIONS_DB
from grpc_gen.generated import user_pb2_grpc, user_pb2, subscription_pb2_grpc, subscription_pb2
from orchestrator.orchestrator import Orchestrator


class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.orchestrator = Orchestrator()

    async def GetUserDetails(self, request: user_pb2.UserRequest, context: ServicerContext) -> user_pb2.UserResponse:
        user_id = request.user_id
        user_data = USER_DB.get(user_id)

        if user_data:
            return user_pb2.UserResponse(
                user_id=user_data["user_id"],
                name=user_data["name"],
                email=user_data["email"]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_pb2.UserResponse()


class SubscriptionService(subscription_pb2_grpc.SubscriptionServiceServicer):
    def __init__(self):
        self.orchestrator = Orchestrator()

    async def GetSubscriptionDetails(self, request: subscription_pb2.SubscriptionRequest, context: ServicerContext) -> subscription_pb2.SubscriptionResponse:
        user_id = request.user_id
        subscription_data = SUBSCRIPTIONS_DB.get(user_id)

        if subscription_data:
            return subscription_pb2.SubscriptionResponse(
                user_id=subscription_data["user_id"],
                subscription_type=subscription_data["subscription_type"],
                period=subscription_data["period"]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return subscription_pb2.SubscriptionResponse()


async def start_user_service() -> grpc.aio.Server:
    user_server = grpc.aio.server()
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), user_server)
    user_server.add_insecure_port("[::]:50051")
    print('gRPC USER Server is listening on port 50051')
    await user_server.start()
    return user_server


async def start_subscription_service() -> grpc.aio.Server:
    subscription_server = grpc.aio.server()
    subscription_pb2_grpc.add_SubscriptionServiceServicer_to_server(SubscriptionService(), subscription_server)
    subscription_server.add_insecure_port("[::]:50052")
    print('gRPC SUBSCRIPTION Server is listening on port 50052')
    await subscription_server.start()
    return subscription_server
