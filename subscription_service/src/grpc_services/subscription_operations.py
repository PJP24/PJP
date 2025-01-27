import re
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from subscription_service.src.db.model import Subscription

from datetime import datetime, timedelta

from subscription_service.src.grpc_services.generated.subscription_pb2 import (
    CreateSubscriptionResponse,
    GetSubscriptionsResponse,
    ExtendSubscriptionResponse,
    DeleteSubscriptionResponse,
    ActivateSubscriptionResponse,
    DeactivateSubscriptionResponse,
)

async def create_subscription(session: AsyncSession, user_id: int, subscription_type: str):
    
    subscription = (await session.execute(sa.select(Subscription).filter_by(user_id=user_id))).scalars().first()
    if subscription:
        return CreateSubscriptionResponse(message="Subscription for user with this id already exists.")
    
    if subscription_type == 'monthly':
        end_date = datetime.now().date() + timedelta(days=30)
    elif subscription_type == 'yearly':
        end_date = datetime.now().date() + timedelta(days=365)
    try:
        new_subscription = Subscription(user_id=user_id, end_date=end_date)
        session.add(new_subscription)
        await session.commit()
        return CreateSubscriptionResponse(message="Created.")
    
    except SQLAlchemyError as e:
        return CreateSubscriptionResponse(message=f"Error: {str(e)}.")
    
async def get_subscriptions(session: AsyncSession):
    subscriptions = (await session.execute(sa.select(Subscription))).scalars().all()
    response = GetSubscriptionsResponse()

    for sub in subscriptions:
        response.subscriptions.add(id=str(sub.id), is_active=sub.is_active, end_date=str(sub.end_date), user_id=str(sub.user_id))
    return response

async def extend_subscription(session: AsyncSession, user_id: int, period: str):  
    subscription = (await session.execute(sa.select(Subscription).filter_by(user_id=user_id))).scalars().first()
    if subscription is None:
        return CreateSubscriptionResponse(message="Subscription for user with this id doesn't exist.")
    
    if period == 'month':
        new_end_date = subscription.end_date + timedelta(days=30)
    elif period == 'year':
        new_end_date = subscription.end_date + timedelta(days=365)
    else:
        return ExtendSubscriptionResponse(message="Invalid period. Use 'month' or 'year'.")
    
    try:
        await session.execute(
            sa.update(Subscription)
            .where(Subscription.user_id == user_id)
            .values(end_date=new_end_date)
        )
        await session.commit()
        return ExtendSubscriptionResponse(message=f"Subscription for user with id {user_id} extended to {new_end_date}.")
    
    except SQLAlchemyError as e:
        return ExtendSubscriptionResponse(message=f"Failed to extend subscription: {str(e)}.")

async def delete_subscription(session: AsyncSession, user_id: int):
    subscription = (await session.execute(sa.select(Subscription).filter_by(user_id=user_id))).scalars().first()
    if subscription is None:
        return CreateSubscriptionResponse(message="Subscription for user with this id doesn't exist.")
    
    try:
        await session.delete(subscription)
        return DeleteSubscriptionResponse(message="Subscription deleted.")
    except SQLAlchemyError as e:
        return DeleteSubscriptionResponse(message=f"Failed to delete subscription: {str(e)}.")

async def activate_subscription(session: AsyncSession, user_id: int):
    subscription = (await session.execute(sa.select(Subscription).filter_by(user_id=user_id))).scalars().first()
    if subscription is None:
        return CreateSubscriptionResponse(message="Subscription for user with this id doesn't exist.")
    
    if subscription.is_active:
        return ActivateSubscriptionResponse(message="The subscription for this email is already active.")
    
    try:
        await session.execute(
            sa.update(Subscription)
            .where(Subscription.user_id == user_id)
            .values(is_active=True)
        )
        return ActivateSubscriptionResponse(message=f"Subscription for user with id {user_id} was activated.")
    except SQLAlchemyError as e:
        return ActivateSubscriptionResponse(message=f"Failed to activate subscription: {str(e)}.")

async def deactivate_subscription(session: AsyncSession, email: str):
    subscription = (await session.execute(sa.select(Subscription).filter_by(email=email))).scalars().first()

    if not subscription:
        return DeactivateSubscriptionResponse(message="No subscription with this email.")
    if not subscription.is_active:
        return DeactivateSubscriptionResponse(message="The subscription for this email is not active.")
    
    try:
        await session.execute(
            sa.update(Subscription)
            .where(Subscription.email == email)
            .values(is_active=False)
        )
        return DeactivateSubscriptionResponse(message=f"Subscription for email {email} was deactivated.")
    except SQLAlchemyError as e:
        return DeactivateSubscriptionResponse(message=f"Failed to deactivate subscription: {str(e)}.")

