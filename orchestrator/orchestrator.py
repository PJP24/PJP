from orchestrator.factories import get_user_service_api, get_subscription_service_api
from typing import Dict, Union

class Orchestrator:
    def __init__(self):
        self.get_user_service_api = get_user_service_api()
        self.get_subscription_service_api = get_subscription_service_api()

    async def execute(self, user_id: str) -> Dict[str, Union[str, Dict[str, str]]]:
        user_data = await self.get_user_service_api.fetch_user_data(user_id)
        subscription_data = await self.get_subscription_service_api.fetch_subscription_data(user_id)

        if 'error' in user_data:
            return {"error": user_data['error']}

        if 'error' in subscription_data:
            return {"error": subscription_data['error']}

        combined_response = {
            "user_id": user_data['user_id'],
            "name": user_data['name'],
            "subscription_type": subscription_data['subscription_type'],
            "email": user_data['email'],
            "period": subscription_data['period']
        }
        return combined_response
