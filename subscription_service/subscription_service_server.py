import asyncio
import grpc
from subscription_service.grpc_services.generated.subscription_pb2_grpc import add_SubscriptionServiceServicer_to_server
from subscription_service.db.database import Database
from subscription_service.grpc_services.generated.subscription_pb2_grpc import SubscriptionServiceServicer
from subscription_service.grpc_services.generated.subscription_pb2 import OptOutPolicyResponse
from subscription_service.utils.config import DB_URL
from subscription_service.grpc_services.subscription_db_operations import SubscriptionManager

class SubscriptionService(SubscriptionServiceServicer):
    def __init__(self, database: Database) -> None:
        self.database = database

    async def CreateSubscription(self, request, context):
        async with self.database.session_scope() as session:
            manager = SubscriptionManager(session)
            return await manager.create_subscription(request.email, request.subscription_type)

    async def GetSubscriptions(self, request, context):
        async with self.database.session_scope() as session:
            manager = SubscriptionManager(session)
            return await manager.get_subscriptions()

    async def ChangeSubscription(self, request, context):
        async with self.database.session_scope() as session:
            manager = SubscriptionManager(session)
            return await manager.change_subscription(request.email, request.subscription_type)

    async def DeleteSubscription(self, request, context):
        async with self.database.session_scope() as session:
            manager = SubscriptionManager(session)
            return await manager.delete_subscription(request.email)

    async def ActivateSubscription(self, request, context):
        async with self.database.session_scope() as session:
            manager = SubscriptionManager(session)
            return await manager.activate_subscription(request.email)

    async def OptOutPolicy(self, request, context):
        policy_text = (
            "Opt-Out Policy:\n"
            "Cancel your subscription anytime to stop future charges.\n"
            "1. Press 5\n"
            "2. Enter the email you subscribed with\n"
            "Activate your subscription again anytime."
        )
        return OptOutPolicyResponse(policy=policy_text)

    async def DeactivateSubscription(self, request, context):
        async with self.database.session_scope() as session:
            manager = SubscriptionManager(session)
            return await manager.deactivate_subscription(request.email)

async def serve_subscription(db: Database) -> None:
    server = grpc.aio.server()
    add_SubscriptionServiceServicer_to_server(SubscriptionService(database=db), server)

    server.add_insecure_port("[::]:50052")
    await server.start()
    print("Starting subscription server on 50052...")
    await server.wait_for_termination()

async def main_subscription():
    db = Database(database_url=DB_URL)
    await serve_subscription(db=db)

if __name__ == "__main__":
    asyncio.run(main_subscription())
