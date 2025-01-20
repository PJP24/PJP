import boto3
from src.db.model import Subscription
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

subscriptions_table = dynamodb.Table('Subscriptions')

def get_all_subscriptions_from_dynamodb() -> list[Subscription]:
    response = subscriptions_table.scan()
    return [Subscription(**item) for item in response['Items']]

print(f"Here: {get_all_subscriptions_from_dynamodb()}")
