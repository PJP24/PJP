import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("FASTAPI_BASE_URL")

async def add_subscription_resolver(email: str, subscription_type: str):
    from src.schema import AddSubscriptionResponse
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/subscriptions",
                json={"email": email, "subscription_type": subscription_type},
            )
            response.raise_for_status()  # Automatically raises for non-2xx status codes
            result_info = response.json().get("message", "Unknown result")
            return AddSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error adding subscription: {e}")

async def change_subscription_resolver(email: str, subscription_type: str):
    from src.schema import UpdateSubscriptionResponse
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{BASE_URL}/subscriptions",
                json={"email": email, "subscription_type": subscription_type},
            )
            response.raise_for_status()  # Automatically raises for non-2xx status codes
            result_info = response.json().get("message", "Unknown result")
            return UpdateSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error updating subscription: {e}")

async def delete_subscription_resolver(email: str):
    from src.schema import DeleteSubscriptionResponse
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{BASE_URL}/subscriptions/{email}",
            )
            response.raise_for_status()  # Automatically raises for non-2xx status codes
            result_info = response.json().get("message", "Unknown result")
            return DeleteSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error deleting subscription: {e}")

async def activate_subscription_resolver(email: str):
    from src.schema import ActivateSubscriptionResponse
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/subscriptions/{email}/activate",
            )
            response.raise_for_status()  # Automatically raises for non-2xx status codes
            result_info = response.json().get("message", "Unknown result")
            return ActivateSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error activating subscription: {e}")

async def deactivate_subscription_resolver(email: str):
    from src.schema import DeactivateSubscriptionResponse
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/subscriptions/{email}/deactivate",
            )
            response.raise_for_status()  # Automatically raises for non-2xx status codes
            result_info = response.json().get("message", "Unknown result")
            return DeactivateSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error deactivating subscription: {e}")
