import grpc
import json
from kafka import KafkaProducer
from typing import List
from orchestrator_monolith.src.generated.subscription_pb2_grpc import (
    SubscriptionServiceStub,
)
from orchestrator_monolith.src.generated.subscription_pb2 import (
    GetSubscriptionsRequest,
    CreateSubscriptionRequest,
    ExtendSubscriptionRequest,
    DeleteSubscriptionRequest,
    ActivateSubscriptionRequest,
    DeactivateSubscriptionRequest,
    GetSubscriptionRequest,
)

from orchestrator_monolith.src.generated.user_pb2_grpc import UserManagementStub
from orchestrator_monolith.src.generated.user_pb2 import (
    UserId,
    CreateUserRequest,
    UpdatePassword,
    GetUserIdRequest,
    GetEmailsRequest,
)


class Orchestrator:
    def __init__(self):
        self.user_host = "user_service_container:50051"
        self.subscription_host = "subscription_service_container:50052"
        self.kafka_broker = "broker:9092"
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_broker,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    async def send_to_kafka(self, topic: str, message: dict):
        try:
            self.producer.send(topic, value=message)
            self.producer.flush()
            print(f"Message sent to topic '{topic}': {message}")
        except Exception as e:
            print(f"Failed to send message to Kafka topic '{topic}': {e}")

    async def send_verification_email(self, email: str, username: str):
        try:
            verification_data = {
                "email": email,
                "username": username,
                "message": f"Hi, {username}! Please verify your email to complete the registration.",
            }

            await self.send_to_kafka(
                topic="email_notifications", message=verification_data
            )

            return {
                "status": "success",
                "message": "Verification email sent.",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error sending verification email: {e}",
            }

    async def send_successful_payment_email(self, email: str):
        try:
            notification_data = {
                "email": email,
                "message": "Hi! Your subscription payment was successful.",
            }

            await self.send_to_kafka(
                topic="successful_payment_notifications", message=notification_data
            )
            return {
                "status": "success",
                "message": "Payment confirmation email sent.",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error sending payment email: {e}",
            }

    async def add_user(self, username: str, email: str, password: str):
        try:
            request = CreateUserRequest(
                username=username, email=email, password=password
            )
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                user_data = await stub.CreateUser(request)
                if user_data.status == "success":
                    email_result = await self.send_verification_email(email, username)
                    return {
                        "status": user_data.status,
                        "message": f"{user_data.message} | {email_result['message']}",
                        "username": user_data.username,
                        "email": user_data.email,
                        "id": user_data.id,
                    }
                return {
                    "status": user_data.status,
                    "message": f"{user_data.message}",
                    "username": user_data.username,
                    "email": user_data.email,
                    "id": user_data.id,
                }
        except Exception as e:
            return {"error": f"Error adding user: {str(e)}"}

    async def get_user(self, user_id: int):
        try:
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                user_data = await stub.GetUserDetails(UserId(id=user_id))
                print(user_data)
                subscription = await self.get_subscription(user_id=user_id)
                if not subscription:
                    return {
                        "username": user_data.username,
                        "email": user_data.email,
                    }
                return {
                    "username": user_data.username,
                    "email": user_data.email,
                    "id": subscription["id"],
                    "is_active": subscription["is_active"],
                    "end_date": subscription["end_date"],
                    # "subscription_type" : subscription["subscription_type"],
                }
        except Exception as e:
            return {"error": f"Error fetching user data: {str(e)}"}

    async def update_user_password(
        self, user_id: int, old_password: str, new_password: str
    ):
        try:
            request = UpdatePassword(
                user_id=UserId(id=user_id),
                old_password=old_password,
                new_password=new_password,
            )
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                response = await stub.UpdateUserPassword(request)
                return {"status": response.status, "message": response.message}
        except Exception as e:
            return {"error": f"Error updating user: {str(e)}"}

    async def delete_user(self, user_id: int):
        try:
            request = UserId(id=user_id)
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                response = await stub.DeleteUser(request)
                return {"status": response.status, "message": response.message}
        except Exception as e:
            return {"error": f"Error deleting user: {str(e)}"}

    async def get_user_id_by_email(self, email: str):
        try:
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                request = GetUserIdRequest(email=email)
                user_data = await stub.GetUserId(request)
                return {"status": user_data.status}
        except Exception as e:
            return {"error": f"Error fetching user id: {str(e)}"}

    async def get_users_emails_by_id(self, ids: List[int]):
        try:
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                request = GetEmailsRequest(id=ids)
                response = await stub.GetUsersEmails(request)
                return {"emails": response.email}
        except Exception as e:
            return {"error": f"Error fetching user id: {str(e)}"}

    async def get_all_subscriptions(self):
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = GetSubscriptionsRequest()
                response = await stub.GetSubscriptions(request)
            result = [
                {
                    "id": sub.id,
                    "is_active": sub.is_active,
                    "end_date": sub.end_date,
                    "user_id": sub.user_id,
                }
                for sub in response.subscriptions
            ]
            return result
        except Exception as e:
            return {"status": "error", "message": f"Error fetching subscriptions: {e}"}

    async def add_subscription(self, email: str, subscription_type: str):
        user_id_by_email = await self.get_user_id_by_email(email=email)
        user_id = user_id_by_email["status"]
        if user_id == "error":
            return {"status": "error", "message": "User with this email not found."}
        user_id = int(user_id)
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = CreateSubscriptionRequest(
                    user_id=user_id, subscription_type=subscription_type
                )
                response = await stub.CreateSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {"status": "error", "message": f"Error adding subscription: {e}"}

    async def extend_subscription(self, email: str, period: str):
        user_id_by_email = await self.get_user_id_by_email(email=email)
        user_id = user_id_by_email["status"]
        if user_id == "error":
            return {"status": "error", "message": "User with this email not found."}
        user_id = int(user_id)
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = ExtendSubscriptionRequest(user_id=user_id, period=period)

                response = await stub.ExtendSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {"status": "error", "message": f"Error extending subscription: {e}"}

    async def delete_subscription(self, email: str):
        user_id_by_email = await self.get_user_id_by_email(email=email)
        user_id = user_id_by_email["status"]
        if user_id == "error":
            return {"status": "error", "message": "User with this email not found."}
        user_id = int(user_id)
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = DeleteSubscriptionRequest(user_id=user_id)
                response = await stub.DeleteSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {"status": "error", "message": f"Error deleting subscription: {e}"}

    async def activate_subscription(self, email: str):
        user_id_by_email = await self.get_user_id_by_email(email=email)
        user_id = user_id_by_email["status"]
        if user_id == "error":
            return {"status": "error", "message": "User with this email not found."}
        user_id = int(user_id)
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = ActivateSubscriptionRequest(user_id=user_id)
                response = await stub.ActivateSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {"status": "error", "message": f"Error activating subscription: {e}"}

    async def deactivate_subscription(self, email: str):
        user_id_by_email = await self.get_user_id_by_email(email=email)
        user_id = user_id_by_email["status"]
        if user_id == "error":
            return {"status": "error", "message": "User with this email not found."}
        user_id = int(user_id)
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = DeactivateSubscriptionRequest(user_id=user_id)
                response = await stub.DeactivateSubscription(request)

            return {"status": "success", "message": response.message}
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error deactivating subscription: {e}",
            }

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

    async def pay_subscription(self, email: str, amount: float):
        user_id_by_email = await self.get_user_id_by_email(email=email)
        user_id = user_id_by_email["status"]
        if user_id == "error":
            return {"status": "error", "message": "Subscription not found."}
        subscription = await self.get_subscription(user_id=int(user_id))
        print(subscription)
        if subscription is None:
            return {"status": "error", "message": "Subscription not found."}
        if amount == 20:
            email_result = await self.send_successful_payment_email(email)
            return {
                "status": "success",
                "message": f"Your payment was successful. | {email_result['message']}",
            }
        return {"status": "error", "message": "Unsuccessful payment, please try again."}

    async def get_subscription(self, user_id: int):
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = GetSubscriptionRequest(user_id=user_id)
                response = await stub.GetSubscription(request)
            if response and response.id:
                return {
                    "id": response.id,
                    "is_active": response.is_active,
                    "end_date": response.end_date,
                    "user_id": response.user_id,
                }
            return None
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error getting subscription: {e}",
            }
