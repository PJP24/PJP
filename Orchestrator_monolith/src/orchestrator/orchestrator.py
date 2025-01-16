import grpc
from src.generated.subscription_pb2_grpc import SubscriptionServiceStub
from src.generated.subscription_pb2 import (
    GetSubscriptionsRequest,
    CreateSubscriptionRequest,
    ChangeSubscriptionRequest,
    DeleteSubscriptionRequest,
    ActivateSubscriptionRequest,
    DeactivateSubscriptionRequest,
)

class Orchestrator:
    def __init__(self, user_service_api=None, subscription_service_api=None):
        self.host = "subscription_server_container:50052"

    async def get_all_subscriptions(self):
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = GetSubscriptionsRequest()
                response = await stub.GetSubscriptions(request)

            return [
                {"email": sub.email, "subscription_type": sub.subscription_type, "is_active": sub.is_active}
                for sub in response.subscriptions
            ]
        except Exception as e:
            return {"status": "error", "message": f"Error fetching subscriptions: {e}"}

    async def add_subscription(self, email: str, subscription_type: str):
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = CreateSubscriptionRequest(
                    email=email,
                    subscription_type=subscription_type
                )
                response = await stub.CreateSubscription(request)

            if response.message is not None:
                return {"status": "success", "message": response.message}
            else:
                return {"status": "error", "message": "Error adding subscription"}
        except Exception as e:
            return {"status": "error", "message": f"Error adding subscription: {e}"}

    async def change_subscription(self, email: str, subscription_type: str):
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = ChangeSubscriptionRequest(
                    email=email,
                    subscription_type=subscription_type
                )
                response = await stub.ChangeSubscription(request)

            if response.message is not None:
                return {"status": "success", "message": response.message}
            else:
                return {"status": "error", "message": "Error updating subscription"}
        except Exception as e:
            return {"status": "error", "message": f"Error updating subscription: {e}"}

    async def delete_subscription(self, email: str):
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = DeleteSubscriptionRequest(email=email)
                response = await stub.DeleteSubscription(request)

            if response.message is not None:
                return {"status": "success", "message": response.message}
            else:
                return {"status": "error", "message": "Error deleting subscription"}
        except Exception as e:
            return {"status": "error", "message": f"Error deleting subscription: {e}"}

    async def activate_subscription(self, email: str):
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = ActivateSubscriptionRequest(email=email)
                response = await stub.ActivateSubscription(request)

            if response.message is not None:
                return {"status": "success", "message": response.message}
            else:
                return {"status": "error", "message": "Error activating subscription"}
        except Exception as e:
            return {"status": "error", "message": f"Error activating subscription: {e}"}

    async def deactivate_subscription(self, email: str):
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = DeactivateSubscriptionRequest(email=email)
                response = await stub.DeactivateSubscription(request)

            if response.message is not None:
                return {"status": "success", "message": response.message}
            else:
                return {"status": "error", "message": "Error deactivating subscription"}
        except Exception as e:
            return {"status": "error", "message": f"Error deactivating subscription: {e}"}

    async def get_opt_out_policy(self):
        try:
            policy_text = (
                "Opt-Out Policy:\n"
                "Cancel your subscription anytime to stop future charges.\n"
                "1. Press 5\n"
                "2. Enter the email you subscribed with\n"
                "Activate your subscription again any time."
            )
            return policy_text
        except Exception as e:
            return {"status": "error", "message": f"Error fetching opt-out policy: {e}"}
