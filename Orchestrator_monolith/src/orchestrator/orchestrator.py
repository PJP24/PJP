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
