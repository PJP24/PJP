from subscription_service.src.db.database import Database
from subscription_service.src.grpc_services.generated.subscription_pb2_grpc import SubscriptionServiceServicer
from subscription_service.src.grpc_services.generated.subscription_pb2 import OptOutPolicyResponse

from subscription_service.src.grpc_services.subscription_operations import (
    create_subscription,
    get_subscriptions,
    extend_subscription,
    delete_subscription,
    activate_subscription,
    deactivate_subscription,
)

class SubscriptionService(SubscriptionServiceServicer):
    def __init__(self, database: Database) -> None:
        self.database = database

    async def GetSubscriptions(self, request, context):
        async with self.database.session_scope() as session:
            return await get_subscriptions(session)

    async def CreateSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await create_subscription(session, request.user_id, request.subscription_type)

    async def ExtendSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await extend_subscription(session, request.user_id, request.period)

    async def DeleteSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await delete_subscription(session, request.email)

    async def ActivateSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await activate_subscription(session, request.email)

    async def DeactivateSubscription(self, request, context):
        async with self.database.session_scope() as session:
            return await deactivate_subscription(session, request.email)

    async def OptOutPolicy(self, request, context):
        policy_text = (
            "Opt-Out Policy:\n"
            "Cancel your subscription anytime to stop future charges.\n"
            "1. Press 5\n"
            "2. Enter the email you subscribed with\n"
            "Activate your subscription again any time."
        )
        return OptOutPolicyResponse(policy=policy_text)