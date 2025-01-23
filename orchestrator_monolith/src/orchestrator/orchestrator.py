import grpc
from orchestrator_monolith.src.generated.subscription_pb2_grpc import SubscriptionServiceStub
from orchestrator_monolith.src.generated.subscription_pb2 import (
    GetSubscriptionsRequest,
    CreateSubscriptionRequest,
    ExtendSubscriptionRequest,
    DeleteSubscriptionRequest,
    ActivateSubscriptionRequest,
    DeactivateSubscriptionRequest,
)

from orchestrator_monolith.src.generated.user_pb2_grpc import UserManagementStub
from orchestrator_monolith.src.generated.user_pb2 import Id, User, UpdatePassword, GetUserIdRequest


class Orchestrator:
    def __init__(self):
        self.user_host = "user_service_container:50051"
        self.subscription_host = "subscription_service_container:50052"

    async def get_user(self, user_id: int):
        try:
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                user_data = await stub.read(Id(id=user_id))
                return {"username": user_data.username, "email": user_data.email}
        except Exception as e:
            return {"error": f"Error fetching user data: {str(e)}"}

    async def add_user(self, username: str, email: str, password: str):
        try:
            request = User(username=username, email=email, password=password)
            async with grpc.aio.insecure_channel(self.user_host) as channel:
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
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                response = await stub.update_password(request)
                return {"status": response.status, "message": response.message}
        except Exception as e:
            return {"error": f"Error updating user: {str(e)}"}

    async def delete_user(self, user_id: int):
        try:
            request = Id(id=user_id)
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                response = await stub.delete(request)
                return {"status": response.status, "message": response.message}
        except Exception as e:
            return {"error": f"Error deleting user: {str(e)}"}
        

    async def get_user_id_by_email(self, email: str):
        try:
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                request = GetUserIdRequest(email=email)
                user_data = await stub.get_user_id(request)
                return {"status": user_data.status}
        except Exception as e:
            return {"error": f"Error fetching user id: {str(e)}"}

    async def get_all_subscriptions(self):
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = GetSubscriptionsRequest()
                response = await stub.GetSubscriptions(request)
            result = [
                {"id": sub.id, "is_active": sub.is_active,
                "end_date": sub.end_date, "user_id": sub.user_id}
                for sub in response.subscriptions
            ]
            return result
        except Exception as e:
            return {"status": "error", "message": f"Error fetching subscriptions: {e}"}

    async def add_subscription(self, email: str, subscription_type: str):
        # Check if user with this email exists
        # If user with this email doesn't exist -> Error
        # Else -> return user_id -> go on ...
        user_id = 1

        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = CreateSubscriptionRequest(
                    user_id=user_id,
                    subscription_type=subscription_type
                )
                response = await stub.CreateSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {"status": "error", "message": f"Error adding subscription: {e}"}

    async def extend_subscription(self, email: str, period: str): 
        # Check if user with this email exists
        # If user with this email doesn't exist -> Error
        # Else -> return user_id -> go on ...
        user_id = 1

        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = ExtendSubscriptionRequest(
                    user_id=user_id,
                    period=period 
                )
                response = await stub.ExtendSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {"status": "error", "message": f"Error extending subscription: {e}"}

    async def delete_subscription(self, email: str):

        # Check if user with this email exists
        # If user with this email doesn't exist -> Error
        # Else -> return user_id -> go on ...
        user_id = 1

        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = DeleteSubscriptionRequest(user_id=user_id)
                response = await stub.DeleteSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {"status": "error", "message": f"Error deleting subscription: {e}"}

    async def activate_subscription(self, email: str):
    
        # Check if user with this email exists
        # If user with this email doesn't exist -> Error
        # Else -> return user_id -> go on ...
        user_id = 1

        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = ActivateSubscriptionRequest(user_id=user_id)
                response = await stub.ActivateSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {"status": "error", "message": f"Error activating subscription: {e}"}

    async def deactivate_subscription(self, email: str):
        # Check if user with this email exists
        # If user with this email doesn't exist -> Error
        # Else -> return user_id -> go on ...
        user_id = 1

        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = DeactivateSubscriptionRequest(user_id=user_id)
                response = await stub.DeactivateSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {"status": "error", "message": f"Error deactivating subscription: {e}"}

    async def get_opt_out_policy(self):
        try:
            policy_text = (
                "Opt-Out Policy:"
                "Cancel your subscription anytime to stop future charges."
                "Activate your subscription again any time."
            )
            return policy_text
        except Exception as e:
            return {"status": "error", "message": f"Error fetching opt-out policy: {e}"}
