import grpc
from src.generated import subscription_pb2, subscription_pb2_grpc

class Orchestrator:
    def __init__(self, user_service_api=None, subscription_service_api=None):
        self.host = "subscription_server_container:50052"

    async def get_all_subscriptions(self):
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.GetSubscriptionsRequest()
            response = await stub.GetSubscriptions(request)

        return [{"email": sub.email, "subscription_type": sub.subscription_type, "is_active": sub.is_active} for sub in response.subscriptions]
    
    async def add_subscription(self, email: str, subscription_type: str):
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.CreateSubscriptionRequest(
                email=email,
                subscription_type=subscription_type
            )
            response = await stub.CreateSubscription(request)

        if response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error adding subscription"}

    async def change_subscription(self, email: str, subscription_type: str):
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.ChangeSubscriptionRequest(
                email=email,
                subscription_type=subscription_type
            )
            response = await stub.ChangeSubscription(request)

        if response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error updating subscription"}

    async def delete_subscription(self, email: str):
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.DeleteSubscriptionRequest(
                email=email
            )
            response = await stub.DeleteSubscription(request)

        if response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error deleting subscription"}

    
    async def activate_subscription(self, email: str):
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.ActivateSubscriptionRequest(
                email=email
            )
            response = await stub.ActivateSubscription(request)

        if response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error activating subscription"}
    
    async def deactivate_subscription(self, email: str):
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.DeactivateSubscriptionRequest(
                email=email
            )
            response = await stub.DeactivateSubscription(request)

        if response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error deactivating subscription"}

    async def get_opt_out_policy(self):
        policy_text = (
            "Opt-Out Policy:\n"
            "Cancel your subscription anytime to stop future charges.\n"
            "1. Press 5\n"
            "2. Enter the email you subscribed with\n"
            "Activate your subscription again any time."
        )
        return policy_text