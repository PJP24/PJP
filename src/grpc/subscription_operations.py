import re
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.model import Subscription
from src.grpc.generated.subscription_pb2 import (
    CreateSubscriptionResponse,
    GetSubscriptionsResponse,
    ChangeSubscriptionResponse,
    DeleteSubscriptionResponse,
    ActivateSubscriptionResponse,
    DeactivateSubscriptionResponse,
)

def validate_email(email: str) -> bool:
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

async def create_subscription(session: AsyncSession, email: str, subscription_type: str):
    try:
        subscription = (
            await session.execute(sa.select(Subscription).filter_by(email=email))
        ).scalars().first()

        if subscription is not None:
            return CreateSubscriptionResponse(message="\nSubscription with this email already exists.")

        if not validate_email(email):
            return CreateSubscriptionResponse(message="\nInvalid email format")

        session.add(Subscription(email=email, subscription_type=subscription_type))
        await session.commit()
        return CreateSubscriptionResponse(message="\nSubscription created")

    except SQLAlchemyError as e:
        return CreateSubscriptionResponse(message=f"\nFailed to create subscription: {str(e)}")

async def get_subscriptions(session: AsyncSession):
    try:
        subscriptions = (await session.execute(sa.select(Subscription))).scalars().all()

        response = GetSubscriptionsResponse()
        for sub in subscriptions:
            response.subscriptions.add(email=sub.email, subscription_type=sub.subscription_type, is_active=sub.is_active)
        return response
    except SQLAlchemyError as e:
        return GetSubscriptionsResponse(message=f"\nFailed to retrieve subscriptions: {str(e)}")

async def change_subscription(session: AsyncSession, email: str, new_subscription: str):
    try:
        subscription = (
            await session.execute(sa.select(Subscription).filter_by(email=email))
        ).scalars().first()

        if not subscription:
            return ChangeSubscriptionResponse(message="\nNo subscription with this email.")

        subscription.subscription_type = new_subscription
        await session.commit()
        return ChangeSubscriptionResponse(
            message=f"\nSubscription for {email} updated to {new_subscription}."
        )
    except SQLAlchemyError as e:
        return ChangeSubscriptionResponse(message=f"\nFailed to change subscription: {str(e)}")

async def delete_subscription(session: AsyncSession, email: str):
    try:
        subscription = (
            await session.execute(sa.select(Subscription).filter_by(email=email))
        ).scalars().first()

        if not subscription:
            return DeleteSubscriptionResponse(message="\nNo subscription with this email.")

        await session.delete(subscription)
        await session.commit()
        return DeleteSubscriptionResponse(message="\nSubscription deleted.")
    except SQLAlchemyError as e:
        return DeleteSubscriptionResponse(message=f"\nFailed to delete subscription: {str(e)}")

async def activate_subscription(session: AsyncSession, email: str):
    try:
        subscription = (
            await session.execute(sa.select(Subscription).filter_by(email=email))
        ).scalars().first()

        if not subscription:
            return ActivateSubscriptionResponse(message="\nNo subscription with this email.")

        if subscription.is_active:
            return ActivateSubscriptionResponse(message="\nThe subscription for this email is already active.")

        subscription.is_active = True
        await session.commit()
        return ActivateSubscriptionResponse(message=f"\nSubscription for email {email} was activated.")
    except SQLAlchemyError as e:
        return ActivateSubscriptionResponse(message=f"\nFailed to activate subscription: {str(e)}")

async def deactivate_subscription(session: AsyncSession, email: str):
    try:
        subscription = (
            await session.execute(sa.select(Subscription).filter_by(email=email))
        ).scalars().first()

        if not subscription:
            return DeactivateSubscriptionResponse(message="\nNo subscription with this email.")

        if not subscription.is_active:
            return DeactivateSubscriptionResponse(message="\nThe subscription for this email is not active.")

        subscription.is_active = False
        await session.commit()
        return DeactivateSubscriptionResponse(message=f"\nSubscription for email {email} was deactivated.")
    except SQLAlchemyError as e:
        return DeactivateSubscriptionResponse(message=f"\nFailed to deactivate subscription: {str(e)}")
