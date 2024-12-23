from src.database.connection import DynamoDBClient
import logging

class UserRepository:
    def __init__(self, table_name='users', client: DynamoDBClient = None):
        self.dynamodb = client.get_client() if client else DynamoDBClient().get_client()
        try:
            self.dynamodb.tables.all()
        except Exception as e:
            logging.error(f"Failed to connect to DynamoDB: {e}")
            raise
        self.table = self.dynamodb.Table(table_name)

    def get_user_by_user_id(self, user_id: str) -> dict:
        try:
            response = self.table.get_item(Key={'user_id': user_id})
            return response.get('Item', {"error": "User not found"})
        except Exception as e:
            logging.error(f"Error fetching user for user_id {user_id}: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    def add_user(self, user_id: str, name: str, email: str) -> dict:
        try:
            response = self.table.put_item(
                Item={'user_id': user_id, 'name': name, 'email': email}
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {"user_id": user_id, "name": name, "email": email}
            return {"error": "Error adding user to database"}
        except Exception as e:
            logging.error(f"Error adding user: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    def update_user(self, user_id: str, name: str, email: str) -> dict:
        try:
            # Check if the user exists
            existing_user = self.get_user_by_user_id(user_id)
            if "error" in existing_user:
                return {"error": f"User with user_id {user_id} not found"}

            # Try to update the user
            response = self.table.update_item(
                Key={'user_id': user_id},
                UpdateExpression="SET #n = :name, email = :email",
                ExpressionAttributeNames={'#n': 'name'},
                ExpressionAttributeValues={':name': name, ':email': email},
                ReturnValues="UPDATED_NEW"
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                updated_attributes = response.get('Attributes', {})
                return {
                    "user_id": user_id,
                    "name": updated_attributes.get('name', name),
                    "email": updated_attributes.get('email', email)
                }
            return {"error": "Error updating user in database"}

        except Exception as e:
            logging.error(f"Error updating user with user_id {user_id}: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    def delete_user(self, user_id: str) -> dict:
        try:
            response = self.table.delete_item(Key={'user_id': user_id})
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {"message": f"User with user_id {user_id} deleted successfully"}
            return {"error": "Error deleting user from database"}
        except Exception as e:
            logging.error(f"Error deleting user with user_id {user_id}: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}
