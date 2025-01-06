import logging
from src.logger.logging_handler import DynamoDBLogHandler
from src.orchestrator.factories import user_service_api as user_service_api_factory
from src.orchestrator.factories import subscription_service_api as subscription_service_api_factory

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
dynamo_handler = DynamoDBLogHandler()
formatter = logging.Formatter('%(message)s')
dynamo_handler.setFormatter(formatter)
logger.addHandler(dynamo_handler)

class Orchestrator:
    def __init__(self, user_service_api=None, subscription_service_api=None):
        self.user_service_api = user_service_api or user_service_api_factory()
        self.subscription_service_api = subscription_service_api or subscription_service_api_factory()

    # Subscriptions
    async def get_all_subscriptions(self):
        try:
            subscriptions = await self.subscription_service_api.fetch_all_subscriptions()
            return subscriptions
        except Exception as e:
            return {'error': f"Error fetching subscriptions data: {str(e)}"}
    
    async def add_subscription(self, email: str, subscription_type: str):
        try:
            subscription_data = await self.subscription_service_api.add_subscription(email, subscription_type)
            return subscription_data
        except Exception as e:
            return {"error": f"Error adding subscription: {str(e)}"}

    async def change_subscription(self, email: str, subscription_type: str):
        try:
            changed_subscription = await self.subscription_service_api.change_subscription(email, subscription_type)
            return changed_subscription
        except Exception as e:
            return {"error": f"Error changing subscription: {str(e)}"}

    async def delete_subscription(self, email: str):
        try:
            deleted_subscription = await self.subscription_service_api.delete_subscription(email)
            if "error" in deleted_subscription:
                return {"error": deleted_subscription["error"]}

            return deleted_subscription
        except Exception as e:
            return {"error": f"Error deleting subscription: {str(e)}"}
    
    async def activate_subscription(self, email: str):
        try:
            response = await self.subscription_service_api.activate_subscription(email)
            if "error" in response:
                return {"status": "error", "message": response["error"]}
            
            return {"status": response["status"]}
        except Exception as e:
            return {"status": "error", "message": f"Error activating subscription: {str(e)}"}
    
    async def deactivate_subscription(self, email: str):
        try:
            response = await self.subscription_service_api.deactivate_subscription(email)
            if "error" in response:
                return {"status": "error", "message": response["error"]}
            
            return {"status": response["status"]}
        except Exception as e:
            return {"status": "error", "message": f"Error activating subscription: {str(e)}"}

    async def get_opt_out_policy(self):
        try:
            policy_text = await self.subscription_service_api.fetch_opt_out_policy()
            return policy_text
        except Exception as e:
            return {"error": f"Error fetching opt-out policy: {str(e)}"}
            
    # Users
    async def get_user(self, user_id: str):
        logger.info(f"Fetching user data for user_id: {user_id}")
        try:
            user_data = await self.user_service_api.fetch_user_data(user_id)
            logger.info(f"Received user data: {user_data}")
            return user_data
        except Exception as e:
            logger.error(f"Error fetching user data for user_id {user_id}: {e}")
            return {"error": f"Error fetching user data: {str(e)}"}

    async def add_user(self, name: str, email: str):
        logger.info(f"Adding user with name: {name}, email: {email}")
        try:
            user_data = await self.user_service_api.add_user(name, email)
            if "error" in user_data:
                logger.error(f"Error adding user: {user_data['error']}")
                return {"error": user_data["error"]}

            logger.info(f"User added successfully: {user_data}")
            return user_data
        except Exception as e:
            logger.error(f"Error adding user with name {name} and email {email}: {e}")
            return {"error": f"Error adding user: {str(e)}"}

    async def update_user(self, user_id: str, name: str, email: str):
        logger.info(f"Updating user with user_id: {user_id}, name: {name}, email: {email}")
        try:
            user_data = await self.user_service_api.update_user(user_id, name, email)
            if "error" in user_data:
                logger.error(f"Error updating user: {user_data['error']}")
                return {"error": user_data["error"]}

            logger.info(f"User updated successfully: {user_data}")
            return user_data
        except Exception as e:
            logger.error(f"Error updating user with user_id {user_id}, name {name}, and email {email}: {e}")
            return {"error": f"Error updating user: {str(e)}"}

    async def delete_user(self, user_id: str):
        logger.info(f"Deleting user with user_id: {user_id}")
        try:
            user_data = await self.user_service_api.delete_user(user_id)
            if "error" in user_data:
                logger.error(f"Error deleting user: {user_data['error']}")
                return {"error": user_data["error"]}

            logger.info(f"User deleted successfully: {user_data}")
            return user_data
        except Exception as e:
            logger.error(f"Error deleting user with user_id {user_id}: {e}")
            return {"error": f"Error deleting user: {str(e)}"}
