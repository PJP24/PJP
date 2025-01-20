import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("FASTAPI_BASE_URL")

async def add_subscription_resolver(email: str, subscription_type: str):
    from src.schema import AddSubscriptionResponse
    try:
        url = f"{BASE_URL}/subscriptions"
        async with httpx.AsyncClient() as client:
            request = await client.post(url, json={"email": email, "subscription_type": subscription_type})
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return AddSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error adding subscription: {e}")

async def extend_subscription_resolver(email: str, period: str):
    from src.schema import ExtendSubscriptionResponse
    try:
        url = f"{BASE_URL}/subscriptions"
        async with httpx.AsyncClient() as client:
            request = await client.put(url, json={"email": email, "period": period})
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return ExtendSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error extending subscription: {e}")

async def delete_subscription_resolver(email: str):
    from src.schema import DeleteSubscriptionResponse
    try:
        url = f"{BASE_URL}/subscriptions/{email}"
        async with httpx.AsyncClient() as client:
            request = await client.delete(url)
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return DeleteSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error deleting subscription: {e}")

async def activate_subscription_resolver(email: str):
    from src.schema import ActivateSubscriptionResponse
    try:
        url = f"{BASE_URL}/subscriptions/{email}/activate"
        async with httpx.AsyncClient() as client:
            request = await client.post(url)
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return ActivateSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error activating subscription: {e}")

async def deactivate_subscription_resolver(email: str):
    from src.schema import DeactivateSubscriptionResponse
    try:
        url = f"{BASE_URL}/subscriptions/{email}/deactivate"
        async with httpx.AsyncClient() as client:
            request = await client.post(url)
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return DeactivateSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error deactivating subscription: {e}")
