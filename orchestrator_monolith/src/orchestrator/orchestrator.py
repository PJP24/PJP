import grpc
import json
import logging
from datetime import datetime, timedelta
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
from kafka import KafkaProducer
from typing import List

from orchestrator_monolith.src.generated.subscription_pb2_grpc import SubscriptionServiceStub
from orchestrator_monolith.src.generated.subscription_pb2 import (
    GetSubscriptionsRequest,
    GetExpiringSubscriptionsRequest,
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

    async def activate_subscription(self, email: str, amount: float):
        user_id_by_email = await self.get_user_id_by_email(email=email)
        user_id = user_id_by_email.get("status")

        if user_id == "error":
            return {"status": "error", "message": "User with this email not found."}

        user_id = int(user_id)
        user = await self.get_user(user_id=user_id)
        username = user.get("username")

        subscriptions = await self.get_all_subscriptions()
        subscription = next((sub for sub in subscriptions if int(sub["user_id"]) == user_id), None)

        if not subscription:
            return {"status": "error", "message": "No active subscription found for the user."}

        required_amount = 20 if subscription["subscription_type"] == "monthly" else 100

        if amount != required_amount:
            email_result = await self.send_unsuccessful_payment_email(email=email, username=username)
            return {
                "status": "error",
                "message": f"For a {subscription['subscription_type']} subscription, the payment must be {required_amount} Mongolian tugriks. | {email_result['message']}"
            }

        try:
            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                response = await stub.ActivateSubscription(ActivateSubscriptionRequest(user_id=user_id))
                status = getattr(response, "status", "unknown")
                message = getattr(response, "message", "No message provided")
                email_result = await self.send_successful_payment_email(email=email, username=username)
                return {
                    "status": status,
                    "message": f"{message} | {email_result['message']}",
                    "subscription_type": subscription["subscription_type"],
                    "required_amount": required_amount
                }
        except Exception as e:
            logger.error(f"Error activating subscription: {e}")
            email_result = await self.send_unsuccessful_payment_email(email=email, username=username)
            return {"status": "error", "message": f"Error activating subscription: {e} | {email_result['message']}"}

    async def add_user(self, username: str, email: str, password: str):
        try:
            request = CreateUserRequest(username=username, email=email, password=password)

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
                else:
                    return {
                        "status": user_data.status,
                        "message": f"Error: {user_data.message}. Please try a different username or email.",
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
                }
        except Exception as e:
            return {"error": f"Error fetching user data: {str(e)}"}

    async def update_user_password(self, user_id: int, old_password: str, new_password: str):
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
                    "subscription_type": sub.subscription_type

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

    async def extend_subscription(self, email: str, amount: int):
        user_id_by_email = await self.get_user_id_by_email(email=email)
        user_id = user_id_by_email["status"]
        if user_id == "error":
            return {"status": "error", "message": "User with this email not found."}
        user_id = int(user_id)


        if amount == 20:
            period = 'monthly'
        elif amount == 100:
            period = 'yearly'
        else:
            return {
                "status": "error",
                "message": f"Invalid payment amount. Expected 20 for 1 month or 100 for 1 year. Received: {amount}."
            }

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
                    "subscription_type": response.subscription_type,
                }
            return None
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error getting subscription: {e}",
            }



    async def send_verification_email(self, email: str, username: str):
        try:
            notification_data = {
                "email": email,
                "username": username,
                "message": f"Hi, {username}! Please verify your email to complete the registration.",
            }

            await self.send_to_kafka(
                topic="email_notifications", message=notification_data
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

    async def send_successful_payment_email(self, email: str, username: str):
        try:
            notification_data = {
                "email": email,
                "username": username,
                "message": f"Hi {username}! Your subscription payment was successful.",
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

    async def send_unsuccessful_payment_email(self, email: str, username: str):
        try:
            notification_data = {
                "email": email,
                "username": username,
                "message": f"Hi {username}, unfortunately, your subscription payment was unsuccessful. Please try again.",
            }

            await self.send_to_kafka(
                topic="unsuccessful_payment_notifications", message=notification_data
            )
            return {
                "status": "success",
                "message": "Payment failure email sent.",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error sending payment failure email: {e}",
            }

    async def send_subscription_expiration_notification(self, email: str, end_date: str):
        try:
            notification_data = {
                "email": email,
                "message": f"Hi, {email}! Your subscription is expiring on {end_date}. Renew it before {end_date}!",
            }

            await self.send_to_kafka(topic="expiring_subscriptions", message=notification_data)

            return {
                "status": "success",
                "message": f"Notification sent to {email} about subscription expiring on {end_date}.",
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error sending subscription expiration notification to {email}: {e}",
            }

    async def send_emails_for_expiring_subscriptions(self):
        try:
            logger.info("Starting to send emails for expiring subscriptions")

            async with grpc.aio.insecure_channel(self.subscription_host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = GetExpiringSubscriptionsRequest()
                logger.info("Fetching expiring subscriptions from subscription service...")
                response = await stub.GetExpiringSubscriptions(request)

            if not response.subscriptions:
                logger.info("No expiring subscriptions found.")
                return {"status": "success", "message": "No expiring subscriptions found."}

            logger.info(f"Found {len(response.subscriptions)} expiring subscriptions")

            for sub in response.subscriptions:
                user = await self.get_user(int(sub.user_id))
                if 'error' in user:
                    logger.error(f"Error fetching user: {user['error']}")
                    continue

                email = user['email']
                logger.info(f"Sending email to {email} about subscription expiring on {sub.end_date}")

                notification_result = await self.send_subscription_expiration_notification(
                    email=email, end_date=sub.end_date
                )

                if notification_result['status'] == 'error':
                    return notification_result

            return {"status": "success", "message": "Emails sent for expiring subscriptions."}

        except Exception as e:
            logger.error(f"Error sending expiring subscription notifications: {e}")
            return {"status": "error", "message": f"Error sending expiring subscription notifications: {e}"}

