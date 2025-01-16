import re
import sqlalchemy as sa
import os
from dotenv import load_dotenv

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
    # GetSubscriptionsDynamoDBResponse,
    # CreateSubscriptionDynamoDBResponse,
    # DeleteSubscriptionDynamoDBRequest,
    # ChangeSubscriptionTypeDynamoDBRequest,
)



# from src.db.database import Database
# import boto3
# import asyncio

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Connect to DynamoDB
# dynamodb = boto3.resource(
#     'dynamodb',
#     region_name=AWS_REGION,
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
# )

def validate_email(email: str) -> bool:
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

async def create_subscription(session: AsyncSession, email: str, subscription_type: str):
    if not validate_email(email):
        return CreateSubscriptionResponse(message="Invalid email.")
    subscription = (await session.execute(sa.select(Subscription).filter_by(email=email))).scalars().first()
    if subscription:
        return CreateSubscriptionResponse(message="Subscription exists.")
    
    try:        
        session.add(Subscription(email=email, subscription_type=subscription_type))
        return CreateSubscriptionResponse(message="Created.")
    except SQLAlchemyError as e:
        return CreateSubscriptionResponse(message=f"Error: {str(e)}.")
    
async def get_subscriptions(session: AsyncSession):
    subscriptions = (await session.execute(sa.select(Subscription))).scalars().all()

    response = GetSubscriptionsResponse()

    for sub in subscriptions:
        response.subscriptions.add(email=sub.email, subscription_type=sub.subscription_type, is_active=sub.is_active)
    return response

async def change_subscription(session: AsyncSession, email: str, new_subscription: str):

    subscription = (await session.execute(sa.select(Subscription).filter_by(email=email))).scalars().first()

    if subscription is None:
        return ChangeSubscriptionResponse(message="No subscription with this email.")

    if subscription.subscription_type == new_subscription:
        return ChangeSubscriptionResponse(message=f"Subscription for {email} is already {new_subscription}.")

    try:
        await session.execute(sa.update(Subscription).where(Subscription.email == email).values(subscription_type=new_subscription))
        return ChangeSubscriptionResponse(message=f"Subscription for {email} updated to {new_subscription}.")
    
    except SQLAlchemyError as e:
        return ChangeSubscriptionResponse(message=f"Failed to change subscription: {str(e)}.")

async def delete_subscription(session: AsyncSession, email: str):
    subscription = (await session.execute(sa.select(Subscription).filter_by(email=email))).scalars().first()
    if not subscription:
        return DeleteSubscriptionResponse(message="No subscription with this email.")
    
    try:
        await session.delete(subscription)
        return DeleteSubscriptionResponse(message="Subscription deleted.")
    except SQLAlchemyError as e:
        return DeleteSubscriptionResponse(message=f"Failed to delete subscription: {str(e)}.")

async def activate_subscription(session: AsyncSession, email: str):
    subscription = (await session.execute(sa.select(Subscription).filter_by(email=email))).scalars().first()

    if not subscription:
        return ActivateSubscriptionResponse(message="No subscription with this email.")
    if subscription.is_active:
        return ActivateSubscriptionResponse(message="The subscription for this email is already active.")
    
    try:
        await session.execute(
            sa.update(Subscription)
            .where(Subscription.email == email)
            .values(is_active=True)
        )
        return ActivateSubscriptionResponse(message=f"Subscription for email {email} was activated.")
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

# async def get_subscriptions_dynamodb(session: AsyncSession):
#     subscriptions_table = dynamodb.Table('Subscriptions')

#     response = subscriptions_table.scan()

#     subscriptions = [Subscription(**item) for item in response['Items']]

#     response = GetSubscriptionsDynamoDBResponse()
#     for sub in subscriptions:
#         response.subscriptions.add(email=sub.email, subscription_type=sub.subscription_type, is_active=sub.is_active)
#     return response

# async def create_subscription_dynamodb(session: AsyncSession, email: str, subscription_type: str, is_active: bool):
#     subscriptions_table = dynamodb.Table('Subscriptions')
#     try:
#         subscriptions_table.put_item(Item={'email': email, 'subscription_type': subscription_type, 'is_active': is_active})
#         return CreateSubscriptionResponse(message=f"Subscription for {email} created successfully in DynamoDB.")
#     except Exception as e:
#         return CreateSubscriptionResponse(message=f"Error creating subscription: {str(e)}")


# async def delete_subscription_dynamodb(session: AsyncSession, email: str):
#     subscriptions_table = dynamodb.Table('Subscriptions')
#     try:
#         item_search = subscriptions_table.get_item(Key={'email': email})
        
#         if 'Item' not in item_search:
#             return DeleteSubscriptionDynamoDBResponse(message="No subscription found.")
        
#         subscriptions_table.delete_item(Key={'email': email})

#         return DeleteSubscriptionDynamoDBResponse(message="\nSubscription deleted from DynamoDB.")
    
#     except Exception as e:
#         return DeleteSubscriptionDynamoDBResponse(message=f"\nFailed to delete subscription from DynamoDB: {str(e)}.")

# async def change_subscription_type_dynamodb(session: AsyncSession, email: str, new_subscription_type: str):

#     subscriptions_table = dynamodb.Table('Subscriptions')

#     item_search = subscriptions_table.get_item(Key={'email': email})
        
#     if 'Item' not in item_search:
#         return ChangeSubscriptionTypeDynamoDBResponse(message="No subscription found.")
        
#     subscriptions_table.update_item(
#         Key={'email': email},
#         UpdateExpression="set subscription_type = :s",
#         ExpressionAttributeValues={":s": new_subscription_type},
#     )

#     return ChangeSubscriptionTypeDynamoDBResponse(message=f"Subscription type for {email} updated in DynamoDB.")