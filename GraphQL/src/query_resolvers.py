import asyncio
import httpx


async def get_user_details(user_id: int):
    from src.schema import User

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://fast-api:8000/users/user_details/{user_id}"
            )
            print(response)
            user_data = response.json()
            if user_data is None:
                print("User not found.")
                return None
            return User(**user_data)
        except Exception as e:
            print(f"Exception in get_user_details: {e}")
            return None
