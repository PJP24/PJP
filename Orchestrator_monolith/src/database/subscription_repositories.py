from src.database.connection import DynamoDBClient
import logging

class SubscriptionRepository:
    def __init__(self, table_name='subscriptions', client: DynamoDBClient = None):
        self.dynamodb = client.get_client() if client else DynamoDBClient().get_client()
        try:
            self.dynamodb.tables.all()
        except Exception as e:
            logging.error(f"Failed to connect to DynamoDB: {e}")
            raise
        self.table = self.dynamodb.Table(table_name)

    def get_subscription_by_user_id(self, user_id: str) -> dict:
        try:
            response = self.table.get_item(Key={'user_id': user_id})
            return response.get('Item', {"error": "User not found"})
        except Exception as e:
            logging.error(f"Error fetching subscription for user_id {user_id}: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    def add_subscription(self, user_id: str, subscription_type: str, period: str) -> dict:
        try:
            response = self.table.put_item(
                Item={'user_id': user_id, 'subscription_type': subscription_type, 'period': period}
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {"user_id": user_id, "subscription_type": subscription_type, "period": period}
            return {"error": "Error adding user to database"}
        except Exception as e:
            logging.error(f"Error adding user: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}
