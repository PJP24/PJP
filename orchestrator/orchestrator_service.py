import grpc
from orchestrator.generated.user_pb2_grpc import UserManagementStub
from orchestrator.generated.user_pb2 import Id, User, UpdatePassword
from orchestrator.generated import subscription_pb2, subscription_pb2_grpc


class OrchestratorService:
    def __init__(self):
        self.user_service_host = "user_server_service:50051"
        self.subscription_service_host = "subscription_server_service:50052"

    async def get_user(self, user_id: int):
        try:
            async with grpc.aio.insecure_channel(self.user_service_host) as channel:
                stub = UserManagementStub(channel)
                user_data = await stub.read(Id(id=user_id))
                return {"username": user_data.username, "email": user_data.email}
        except Exception as e:
            return {"error": f"Error fetching user data: {str(e)}"}

    async def add_user(self, username: str, email: str, password: str):
        try:
            request = User(username=username, email=email, password=password)
            async with grpc.aio.insecure_channel(self.user_service_host) as channel:
                stub = UserManagementStub(channel)
                user_data = await stub.create(request)
                return {
                    "status": user_data.status,
                    "message": user_data.message,
                    "username": user_data.username,
                    "email": user_data.email,
                }
        except Exception as e:
            return {"error": f"Error adding user: {str(e)}"}

    async def update_user_password(self, user_id: int, old_password: str, new_password: str):
        try:
            request = UpdatePassword(
                user_id=Id(id=user_id),
                old_password=old_password,
                new_password=new_password,
            )
            async with grpc.aio.insecure_channel(self.user_service_host) as channel:
                stub = UserManagementStub(channel)
                response = await stub.update_password(request)
                return {"status": response.status, "message": response.message}
        except Exception as e:
            return {"error": f"Error updating user: {str(e)}"}

    async def delete_user(self, user_id: int):
        try:
            request = Id(id=user_id)
            async with grpc.aio.insecure_channel(self.user_service_host) as channel:
                stub = UserManagementStub(channel)
                response = await stub.delete(request)
                return {"status": response.status, "message": response.message}
        except Exception as e:
            return {"error": f"Error deleting user: {str(e)}"}

    async def get_all_subscriptions(self):
        async with grpc.aio.insecure_channel(self.subscription_service_host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.GetSubscriptionsRequest()
            response = await stub.GetSubscriptions(request)

        subscriptions = []
        for sub in response.subscriptions:
            subscriptions.append({
                "email": sub.email,
                "subscription_type": sub.subscription_type,
                "is_active": sub.is_active
            })
        return subscriptions

    async def add_subscription(self, email: str, subscription_type: str):
        async with grpc.aio.insecure_channel(self.subscription_service_host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.CreateSubscriptionRequest(
                email=email,
                subscription_type=subscription_type
            )
            response = await stub.CreateSubscription(request)

        if hasattr(response, 'message') and response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error adding subscription"}

    async def change_subscription(self, email: str, subscription_type: str):
        async with grpc.aio.insecure_channel(self.subscription_service_host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.ChangeSubscriptionRequest(
                email=email,
                subscription_type=subscription_type
            )
            response = await stub.ChangeSubscription(request)

        if hasattr(response, 'message') and response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error updating subscription"}

    async def delete_subscription(self, email: str):
        async with grpc.aio.insecure_channel(self.subscription_service_host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.DeleteSubscriptionRequest(
                email=email
            )
            response = await stub.DeleteSubscription(request)

        if hasattr(response, 'message') and response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error deleting subscription"}

    async def activate_subscription(self, email: str):
        async with grpc.aio.insecure_channel(self.subscription_service_host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.ActivateSubscriptionRequest(
                email=email
            )
            response = await stub.ActivateSubscription(request)

        if hasattr(response, 'message') and response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error activating subscription"}

    async def deactivate_subscription(self, email: str):
        async with grpc.aio.insecure_channel(self.subscription_service_host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.DeactivateSubscriptionRequest(
                email=email
            )
            response = await stub.DeactivateSubscription(request)

        if hasattr(response, 'message') and response.message:
            return {"status": "success", "message": response.message}
        else:
            return {"status": "error", "message": "Error deactivating subscription"}

    async def get_opt_out_policy(self):
        policy_text = (
            "Opt-Out Policy:"
            "Cancel your subscription anytime to stop future charges."
            "1. Press 5"
            "2. Enter the email you subscribed with"
            "Activate your subscription again any time."
        )
        return policy_text
