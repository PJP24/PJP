import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("FASTAPI_BASE_URL")

async def add_subscription_resolver(email: str, subscription_type: str):
    from GraphQL.src.schema import AddSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/subscriptions",
            json={"email": email, "subscription_type": subscription_type},
        )
        if response.status_code != 200:
            raise Exception(f"Failed to add subscription: {response.status_code} {response.text}")
        result_info = response.json().get("message", "Unknown result")
        return AddSubscriptionResponse(result_info=result_info)

async def change_subscription_resolver(email: str, subscription_type: str):
    from GraphQL.src.schema import UpdateSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BASE_URL}/subscriptions",
            json={"email": email, "subscription_type": subscription_type},
        )
        if response.status_code != 200:
            raise Exception(f"Failed to update subscription: {response.status_code} {response.text}")
        result_info = response.json().get("message", "Unknown result")
        return UpdateSubscriptionResponse(result_info=result_info)

async def delete_subscription_resolver(email: str):
    from GraphQL.src.schema import DeleteSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{BASE_URL}/subscriptions/{email}",
        )
        if response.status_code != 200:
            raise Exception(f"Failed to delete subscription: {response.status_code} {response.text}")
        result_info = response.json().get("message", "Unknown result")
        return DeleteSubscriptionResponse(result_info=result_info)

async def activate_subscription_resolver(email: str):
    from GraphQL.src.schema import ActivateSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/subscriptions/{email}/activate",
        )
        if response.status_code != 200:
            raise Exception(f"Failed to activate subscription: {response.status_code} {response.text}")
        result_info = response.json().get("message", "Unknown result")
        return ActivateSubscriptionResponse(result_info=result_info)

async def deactivate_subscription_resolver(email: str):
    from GraphQL.src.schema import DeactivateSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/subscriptions/{email}/deactivate",
        )
        if response.status_code != 200:
            raise Exception(f"Failed to deactivate subscription: {response.status_code} {response.text}")
        result_info = response.json().get("message", "Unknown result")
        return DeactivateSubscriptionResponse(result_info=result_info)
