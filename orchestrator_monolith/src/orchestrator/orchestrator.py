import grpc
import json
from kafka import KafkaProducer
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
from orchestrator_monolith.src.generated.user_pb2 import Id, User, UpdatePassword


class Orchestrator:
    def __init__(self):
        self.user_host = "user_service_container:50051"
        self.subscription_host = "subscription_service_container:50052"
        self.kafka_broker = "broker:9092"
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_broker,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def send_to_kafka(self, topic: str, message: dict):
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

            self.send_to_kafka(topic="email_notifications", message=verification_data)

            return {
                "status": "success",
                "message": "Verification email sent.",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error sending verification email: {e}",
            }

    async def add_user(self, username: str, email: str, password: str):
        try:
            request = User(username=username, email=email, password=password)
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                user_data = await stub.create(request)

            email_result = await self.send_verification_email(email, username)

            return {
                "status": user_data.status,
                "message": f"{user_data.message} | {email_result['message']}",
                "username": user_data.username,
                "email": user_data.email,
            }
        except Exception as e:
            return {"error": f"Error adding user: {str(e)}"}

    async def get_user(self, user_id: int):
        try:
            async with grpc.aio.insecure_channel(self.user_host) as channel:
                stub = UserManagementStub(channel)
                user_data = await stub.read(Id(id=user_id))
                return {"username": user_data.username, "email": user_data.email}
        except Exception as e:
            return {"error": f"Error fetching user data: {str(e)}"}

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

    async def get_all_subscriptions(self):
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = GetSubscriptionsRequest()
                response = await stub.GetSubscriptions(request)
                print("Raw response:", response)
                print("Subscriptions:", response.subscriptions)

            result = [
                {"email": sub.email, "subscription_type": sub.subscription_type, "is_active": sub.is_active,
                 "end_date": sub.end_date}
                for sub in response.subscriptions
            ]
            return result
        except Exception as e:
            return {"status": "error", "message": f"Error fetching subscriptions: {e}"}

    async def add_subscription(self, email: str, subscription_type: str):
        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
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
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
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
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
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
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
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
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
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

