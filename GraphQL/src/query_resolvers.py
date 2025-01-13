import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


async def get_user_details(user_id: int):
    from src.schema import User

    url = f"{BASE_URL}/user_details/{user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            user_data = response.json()
            return User(**user_data)
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Exception in get_user_details: {e}")
            return None
