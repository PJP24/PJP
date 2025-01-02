import grpc
from src.generated.subscription_pb2_grpc import SubscriptionServiceStub
from src.generated.subscription_pb2 import (
    GetSubscriptionsRequest,
    CreateSubscriptionRequest,
    ExtendSubscriptionRequest,
    DeleteSubscriptionRequest,
    ActivateSubscriptionRequest,
    DeactivateSubscriptionRequest,
)

# import logging
# from src.logger.logging_handler import DynamoDBLogHandler
from src.orchestrator.factories import user_service_api as user_service_api_factory
from src.orchestrator.factories import subscription_service_api as subscription_service_api_factory

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# dynamo_handler = DynamoDBLogHandler()
# formatter = logging.Formatter('%(message)s')
# dynamo_handler.setFormatter(formatter)
# logger.addHandler(dynamo_handler)


class Orchestrator:
    def __init__(self, user_service_api=None, subscription_service_api=None):
        self.host = "subscription_server_container:50052"

    async def get_all_subscriptions(self):
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = GetSubscriptionsRequest()
                response = await stub.GetSubscriptions(request)                 
            result = [
                {"email": sub.email, "subscription_type": sub.subscription_type, "is_active": sub.is_active, "end_date": sub.end_date}
                for sub in response.subscriptions
            ]
            return result
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

    async def extend_subscription(self, email: str, period: str): 
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = ExtendSubscriptionRequest(
                    email=email,
                    period=period 
                )
                response = await stub.ExtendSubscription(request)

            if response.message is not None:
                return {"status": "success", "message": response.message}
            else:
                return {"status": "error", "message": "Error extending subscription"}
        except Exception as e:
            return {"status": "error", "message": f"Error extending subscription: {e}"}

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
       # import logging
# from src.logger.logging_handler import DynamoDBLogHandler
import grpc
from src.generated.user_pb2_grpc import UserManagementStub
from src.generated.user_pb2 import Id, User, UpdatePassword

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# dynamo_handler = DynamoDBLogHandler()
# formatter = logging.Formatter('%(message)s')
# dynamo_handler.setFormatter(formatter)
# logger.addHandler(dynamo_handler)


class Orchestrator:
    def __init__(self):
        self.host = "grpc-server:50051"

    async def get_user(self, user_id: int):
        # logger.info(f"Fetching user data for user_id: {user_id}")
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = UserManagementStub(channel)
                user_data = await stub.read(Id(id=user_id))
                # logger.info(f"Received user data: {user_data}")
                return {"username": user_data.username, "email": user_data.email}
        except Exception as e:
            # logger.error(f"Error fetching user data for user_id {user_id}: {e}")
            return {"error": f"Error fetching user data: {str(e)}"}

    async def add_user(self, username: str, email: str, password: str):
        # logger.info(f"Adding user with name: {name}, email: {email}")
        try:
            request = User(username=username, email=email, password=password)
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = UserManagementStub(channel)
                user_data = await stub.create(request)
            # if user_data.status == "error":
            #     # logger.error(f"Error adding user: {user_data['error']}")
            #     return {"error": user_data["error"]}

            # logger.info(f"User added successfully: {user_data}")
                return {
                    "status": user_data.status,
                    "message": user_data.message,
                    "username": user_data.username,
                    "email": user_data.email,
                }
        except Exception as e:
            # logger.error(f"Error adding user with name {name} and email {email}: {e}")
            return {"error": f"Error adding user: {str(e)}"}

    async def update_user_password(self, user_id: int, old_password: str, new_password: str):
        # logger.info(f"Updating password for user with id {user_id}")
        try:
            request = UpdatePassword(
                user_id=Id(id=user_id),
                old_password=old_password,
                new_password=new_password,
            )
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = UserManagementStub(channel)
                response = await stub.update_password(request)
            # if user_data.status == "error":
            #     # logger.error(f"Error updating password for user {user_id}")
            #     return {"error": user_data["error"]}

            # logger.info(f"User updated successfully: {user_data}")
                return {"status": response.status, "message": response.message}
        except Exception as e:
            # logger.error(f"Error updating user with user_id {user_id}, name {name}, and email {email}: {e}")
            return {"error": f"Error updating user: {str(e)}"}

    async def delete_user(self, user_id: int):
        # logger.info(f"Deleting user with user_id: {user_id}")
        try:
            request = Id(id=user_id)
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = UserManagementStub(channel)
                response = await stub.delete(request)
            # if response.status == "error":
            #     # logger.error(f"Error deleting user: {user_data['error']}")

            # logger.info(f"User deleted successfully: {user_data}")
                return {"status": response.status, "message": response.message}
        except Exception as e:
            # logger.error(f"Error deleting user with user_id {user_id}: {e}")
            return {"error": f"Error deleting user: {str(e)}"}