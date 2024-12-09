from orchestrator.factories import get_user_service_api

class Orchestrator:
    def __init__(self):
        self.get_user_service_api = get_user_service_api()

    async def execute(self, user_id):
        return await self.get_user_service_api.fetch_user_data(user_id)
