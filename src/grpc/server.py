from src.db.database import Database
from src.grpc.generated.subscription_pb2_grpc import SubscriptionServiceServicer

from src.grpc.subscription_operations import (
    create_subscription,
    get_subscriptions,
    change_subscription,
    delete_subscription,
    activate_subscription,
    deactivate_subscription,
)

class SubscriptionService(SubscriptionServiceServicer):
    def __init__(self, database: Database) -> None:
        self.database = database

    async def CreateSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await create_subscription(session, request.email, request.subscription_type)

    async def GetSubscriptions(self, request, context):
        async with self.database.session_scope() as session:
            return await get_subscriptions(session)

    async def ChangeSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await change_subscription(session, request.email, request.subscription_type)

    async def DeleteSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await delete_subscription(session, request.email)

    async def ActivateSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await activate_subscription(session, request.email)

    async def DeactivateSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await deactivate_subscription(session, request.email)
