from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db.model import Base
import re

from src.grpc.generated.subscription_pb2 import (
    CreateSubscriptionResponse,
    GetSubscriptionsResponse,
    ChangeSubscriptionResponse,
    DeleteSubscriptionResponse,
    ActivateSubscriptionResponse, 
    DeactivateSubscriptionResponse,
)

from src.db.model import Subscription
import sqlalchemy as sa

# Database wrapper
class Database():
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False, future=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def init_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
    def validate_email(self, email: str) -> bool:
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None

    async def create_subscription(self, email: str, subscription_type: str):
        try:            
            async with self.async_session() as session:

                subscription = (await session.execute(sa.select(Subscription).filter_by(email=email))).scalars().first()
                if subscription is not None:
                    return CreateSubscriptionResponse(message="\nSubscription with this email already exists.")

                if not self.validate_email(email):
                    return CreateSubscriptionResponse(message="\nInvalid email format")

                session.add(Subscription(email=email, subscription_type=subscription_type))
                await session.commit()
                return CreateSubscriptionResponse(message="\nSubscription created")

        except SQLAlchemyError as e:
            return CreateSubscriptionResponse(message=f"\nFailed to create subscription: {str(e)}")

    async def get_subscriptions(self):
        try:
            async with self.async_session() as session:
                subscriptions = (await session.execute(sa.select(Subscription))).scalars().all()

            response = GetSubscriptionsResponse()
            for sub in subscriptions:
                response.subscriptions.add(email=sub.email, subscription_type=sub.subscription_type, is_active=sub.is_active)
            return response
        except SQLAlchemyError as e:
            return GetSubscriptionsResponse(message=f"\nFailed to retrieve subscriptions: {str(e)}")

    async def change_subscription(self, email: str, new_subscription: str):
        try:
            async with self.async_session() as session:
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

    async def delete_subscription(self, email: str):
        try:
            async with self.async_session() as session:
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

    async def activate_subscription(self, email: str):
        try:
            async with self.async_session() as session:
                subscription = (
                    await session.execute(sa.select(Subscription).filter_by(email=email))
                ).scalars().first()

                if not subscription:
                    return ChangeSubscriptionResponse(message="\nNo subscription with this email.")
                
                if subscription.is_active:
                    return ChangeSubscriptionResponse(message="\nThe subscription for this email is already active.")

                subscription.is_active = True
                await session.commit()
            
            return ActivateSubscriptionResponse(message=f"\nSubscription for email {email} was activated.")
        except SQLAlchemyError as e:
            return ActivateSubscriptionResponse(message=f"\nFailed to activate subscription: {str(e)}")

    async def deactivate_subscription(self, email: str):
        try:
            async with self.async_session() as session:
                subscription = (
                    await session.execute(sa.select(Subscription).filter_by(email=email))
                ).scalars().first()

                if not subscription:
                    return ChangeSubscriptionResponse(message="\nNo subscription with this email.")
                
                if not subscription.is_active:
                    return ChangeSubscriptionResponse(message="\nThe subscription for this email is not active.")

                subscription.is_active = False
                await session.commit()
            
            return DeactivateSubscriptionResponse(message=f"\nSubscription for email {email} was deactivated.")
        except SQLAlchemyError as e:
            return DeactivateSubscriptionResponse(message=f"\nFailed to deactivate subscription: {str(e)}")



async def init_db(db_url):
    database = Database(database_url=db_url)
    await database.init_database() 
    return database
