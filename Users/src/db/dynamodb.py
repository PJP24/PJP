import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
dynamodb_client = boto3.client("dynamodb", region_name="eu-west-2")
user_activity = dynamodb.Table("UserActivityLogs")
users = dynamodb.Table("Users_Project")


async def create_activity_log(username: str, event_type: str):
    try:
        dynamodb_client.put_item(
            TableName="UserActivityLogs",
            Item={
                "Username": {"S": username},
                "EventType": {"S": event_type},
                "TimeStamp": {"S": datetime.now(timezone.utc).isoformat()},
            },
        )
    except ClientError as e:
        print(f"An error occured: {e}")


async def get_activity_log(username: str):
    try:
        response = user_activity.query(
            KeyConditionExpression="Username = :username",
            ExpressionAttributeValues={":username": username},
        )
        log_history = response.get("Items", [])
        return log_history
    except ClientError as e:
        print(f"An error occured: {e}")


async def create_user(username: str, email: str, password: str):
    try:
        dynamodb_client.put_item(
            TableName="Users_Project",
            Item={
                "Username": {"S": username},
                "Email": {"S": email},
                "Password": {"S": password},
                "TimeStamp": {"S": datetime.now(timezone.utc).isoformat()},
            },
        )
    except ClientError as e:
        print(f"An error occured: {e}")


async def update_user(username: str, password: str):
    try:
        dynamodb_client.update_item(
            TableName="Users_Project",
            Key={"Username": {"S": username}},
            UpdateExpression="SET Password = :password",
            ExpressionAttributeValues={":password": {"S": password}},
        )
    except ClientError as e:
        print(f"An error occured: {e}")


async def delete_user(username: str):
    try:
        dynamodb_client.delete_item(
            TableName="Users_Project", Key={"Username": {"S": username}}
        )
    except ClientError as e:
        print(f"An error occured: {e}")
