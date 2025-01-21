import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("FASTAPI_BASE_URL")

async def get_all_subscriptions_resolver():
    from src.schema import Subscription
    try:
        url = f"{BASE_URL}/subscriptions/subscriptions"
        async with httpx.AsyncClient() as client:
            request = await client.get(url)
            request.raise_for_status()
            raw_subscriptions = request.json().get("subscriptions", [])
            return [Subscription(**sub) for sub in raw_subscriptions]
    except Exception as e:
        raise Exception(f"Error fetching subscriptions: {e}")

async def opt_out_policy_resolver():
    from src.schema import OptOutPolicyResponse
    try:
        url = f"{BASE_URL}/subscriptions/opt-out-policy"
        async with httpx.AsyncClient() as client:
            request = await client.get(url)
            request.raise_for_status()
            policy_text = request.json().get("policy", "Unknown policy")
            return OptOutPolicyResponse(policy=policy_text)
    except Exception as e:
        raise Exception(f"Error fetching opt-out policy: {e}")


async def get_user_details(user_id: int):
    from src.schema import User

    url = f"{BASE_URL}/users/user_details/{user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            user_data = response.json()
            return User(**user_data)
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Exception in get_user_details: {e}")
            return None
