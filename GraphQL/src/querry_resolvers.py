import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("FASTAPI_BASE_URL")

async def get_all_subscriptions_resolver():
    from src.schema import Subscription
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/subscriptions")
        if response.status_code != 200:
            raise Exception(f"Failed to fetch subscriptions: {response.status_code} {response.text}")
        raw_subscriptions = response.json().get("subscriptions", [])
        return [Subscription(**sub) for sub in raw_subscriptions]

async def opt_out_policy_resolver():
    from src.schema import OptOutPolicyResponse
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/opt-out-policy")
        if response.status_code != 200:
            raise Exception(f"Failed to fetch opt-out policy: {response.status_code} {response.text}")
        policy_text = response.json().get("policy", "Unknown policy")
        return OptOutPolicyResponse(policy=policy_text)
