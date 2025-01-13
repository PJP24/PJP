import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

READ_USER_URL = os.getenv("READ_USER_URL")


async def get_user_details(user_id: int):
    from src.schema import User

    async with httpx.AsyncClient() as client:
        try:
            url = READ_USER_URL.format(user_id=user_id)
            response = await client.get(url)
            user_data = response.json()
            return User(**user_data)
        except Exception as e:
            print(f"Exception in get_user_details: {e}")
            return None
