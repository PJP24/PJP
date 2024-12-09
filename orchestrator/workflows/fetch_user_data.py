class FetchUserData:
    def __init__(self, user_service):
        self.user_service = user_service

    async def execute(self, user_id):
        return await self.user_service.fetch_user_data(user_id)
