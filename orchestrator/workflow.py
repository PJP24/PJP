class FetchUserDataWorkflow:
    def __init__(self, user_service):
        self.user_service = user_service

    async def execute(self, user_id: str):
        return await self.user_service.fetch_data(user_id)
