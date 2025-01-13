import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from subscription_service.db.model import Subscription
from subscription_service.utils.validators import validate_email
from subscription_service.grpc_services.generated.subscription_pb2 import (
    CreateSubscriptionResponse,
    GetSubscriptionsResponse,
    ChangeSubscriptionResponse,
    DeleteSubscriptionResponse,
    ActivateSubscriptionResponse,
    DeactivateSubscriptionResponse,
)

class SubscriptionManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_subscription(self, email: str, subscription_type: str):
        try:
            subscription = (
                await self.session.execute(sa.select(Subscription).filter_by(email=email))
            ).scalars().first()

            if subscription:
                return CreateSubscriptionResponse(message="Subscription with this email already exists.")

            if not validate_email(email):
                return CreateSubscriptionResponse(message="Invalid email format.")

            self.session.add(Subscription(email=email, subscription_type=subscription_type))
            return CreateSubscriptionResponse(message="Subscription created.")
        except SQLAlchemyError as e:
            return CreateSubscriptionResponse(message=f"Failed to create subscription: {str(e)}.")

    async def get_subscriptions(self):
        subscriptions = (await self.session.execute(sa.select(Subscription))).scalars().all()

        response = GetSubscriptionsResponse()
        for sub in subscriptions:
            response.subscriptions.add(email=sub.email, subscription_type=sub.subscription_type, is_active=sub.is_active)
        return response

    async def change_subscription(self, email: str, new_subscription: str):
        try:
            subscription = (
                await self.session.execute(sa.select(Subscription).filter_by(email=email))
            ).scalars().first()

            if not subscription:
                return ChangeSubscriptionResponse(message="No subscription with this email.")

            if subscription.subscription_type == new_subscription:
                return ChangeSubscriptionResponse(
                    message=f"Subscription for {email} is already {new_subscription}."
                )

            await self.session.execute(
                sa.update(Subscription)
                .where(Subscription.email == email)
                .values(subscription_type=new_subscription)
            )

            return ChangeSubscriptionResponse(
                message=f"Subscription for {email} updated to {new_subscription}."
            )
        except SQLAlchemyError as e:
            return ChangeSubscriptionResponse(message=f"Failed to change subscription: {str(e)}.")

    async def delete_subscription(self, email: str):
        try:
            subscription = (
                await self.session.execute(sa.select(Subscription).filter_by(email=email))
            ).scalars().first()

            if not subscription:
                return DeleteSubscriptionResponse(message="No subscription with this email.")

            await self.session.delete(subscription)
            return DeleteSubscriptionResponse(message="Subscription deleted.")
        except SQLAlchemyError as e:
            return DeleteSubscriptionResponse(message=f"Failed to delete subscription: {str(e)}.")

    async def activate_subscription(self, email: str):
        try:
            subscription = (
                await self.session.execute(sa.select(Subscription).filter_by(email=email))
            ).scalars().first()

            if not subscription:
                return ActivateSubscriptionResponse(message="No subscription with this email.")

            if subscription.is_active:
                return ActivateSubscriptionResponse(message="The subscription for this email is already active.")

            await self.session.execute(
                sa.update(Subscription)
                .where(Subscription.email == email)
                .values(is_active=True)
            )

            return ActivateSubscriptionResponse(message=f"Subscription for email {email} was activated.")
        except SQLAlchemyError as e:
            return ActivateSubscriptionResponse(message=f"Failed to activate subscription: {str(e)}.")

    async def deactivate_subscription(self, email: str):
        try:
            subscription = (
                await self.session.execute(sa.select(Subscription).filter_by(email=email))
            ).scalars().first()

            if not subscription:
                return DeactivateSubscriptionResponse(message="No subscription with this email.")

            if not subscription.is_active:
                return DeactivateSubscriptionResponse(message="The subscription for this email is not active.")

            await self.session.execute(
                sa.update(Subscription)
                .where(Subscription.email == email)
                .values(is_active=False)
            )

            return DeactivateSubscriptionResponse(message=f"Subscription for email {email} was deactivated.")
        except SQLAlchemyError as e:
            return DeactivateSubscriptionResponse(message=f"Failed to deactivate subscription: {str(e)}.")
