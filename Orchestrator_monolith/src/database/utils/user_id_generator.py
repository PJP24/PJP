import logging
from src.database.connection import DynamoDBClient

class UserIdGenerator:
    def __init__(self, table_name: str, client: DynamoDBClient = None):
        self.table_name = table_name
        self.dynamodb = self._get_dynamodb_client(client)
        self.table = self.dynamodb.Table(table_name)

    def _get_dynamodb_client(self, client: DynamoDBClient = None):
        try:
            return client.get_client() if client else DynamoDBClient().get_client()
        except Exception as e:
            logging.error(f"Failed to connect to DynamoDB: {e}")
            raise

    def get_next_user_id(self) -> str | dict[str, str]:
        try:
            response = self.table.scan(ProjectionExpression="user_id")
            if 'Items' in response and response['Items']:
                user_ids = sorted(
                    [int(item['user_id']) for item in response['Items'] if 'user_id' in item]
                )
                next_user_id = 1
                for user_id in user_ids:
                    if next_user_id == user_id:
                        next_user_id += 1
                    else:
                        break
            else:
                next_user_id = 1
            return str(next_user_id)
        except Exception as e:
            logging.error(f"Error getting next user_id: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

