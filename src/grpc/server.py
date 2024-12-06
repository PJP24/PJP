from src.db.database import Database
from src.grpc.generated.subscription_pb2_grpc import SubscriptionServiceServicer
import grpc
from src.grpc.generated.subscription_pb2_grpc import add_SubscriptionServiceServicer_to_server
from src.grpc.generated.subscription_pb2 import (
    CreateSubscriptionRequest,
    GetSubscriptionsRequest,
    ChangeSubscriptionRequest,
    DeleteSubscriptionRequest,
    ActivateSubscriptionRequest,
    DeactivateSubscriptionRequest, 
)

# gRPC service wrapper
class SubscriptionService(SubscriptionServiceServicer):
    def __init__(self, database: Database) -> None:
        self.database = database
    
    async def CreateSubscription(self, request: CreateSubscriptionRequest, context: grpc.aio.ServicerContext):
        message = await self.database.create_subscription(request.email, request.subscription_type)
        return message

    async def GetSubscriptions(self, request: GetSubscriptionsRequest, context: grpc.aio.ServicerContext):
        message = await self.database.get_subscriptions()
        return message

    async def ChangeSubscription(self, request: ChangeSubscriptionRequest, context: grpc.aio.ServicerContext):
        message = await self.database.change_subscription(request.email, request.subscription_type)  
        return message

    async def DeleteSubscription(self, request: DeleteSubscriptionRequest, context: grpc.aio.ServicerContext):
        message = await self.database.delete_subscription(request.email)
        return message

    async def ActivateSubscription(self, request: ActivateSubscriptionRequest, context: grpc.aio.ServicerContext):
        message = await self.database.activate_subscription(request.email)
        return message

    async def DeactivateSubscription(self, request: DeactivateSubscriptionRequest, context: grpc.aio.ServicerContext):
        message = await self.database.deactivate_subscription(request.email)
        return message


async def start_grpc_server(db: Database) -> None:
    server = grpc.aio.server()
    add_SubscriptionServiceServicer_to_server(SubscriptionService(database=db), server)

    server.add_insecure_port("0.0.0.0:50051") 

    print("Starting server...")
    await server.start()
    await server.wait_for_termination()
