import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("FASTAPI_BASE_URL")

async def get_all_subscriptions_resolver():
    from src.schema import Subscription
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/subscriptions")
            response.raise_for_status() 
            raw_subscriptions = response.json().get("subscriptions", [])
            return [Subscription(**sub) for sub in raw_subscriptions]
    except Exception as e:
        raise Exception(f"Error fetching subscriptions: {e}")

async def opt_out_policy_resolver():
    from src.schema import OptOutPolicyResponse
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/opt-out-policy")
            response.raise_for_status()
            policy_text = response.json().get("policy", "Unknown policy")
            return OptOutPolicyResponse(policy=policy_text)
    except Exception as e:
        raise Exception(f"Error fetching opt-out policy: {e}")
