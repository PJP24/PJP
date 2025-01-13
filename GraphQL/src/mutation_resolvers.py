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

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

ADD_USER_URL = os.getenv("ADD_USER_URL")
UPDATE_PASSWORD_URL = os.getenv("UPDATE_PASSWORD_URL")
DELETE_USER_URL = os.getenv("DELETE_USER_URL")


async def add_user(username: str, email: str, password: str):
    from src.schema import AddUserResponse, User

    async with httpx.AsyncClient() as client:
        try:
            user_data = {"username": username, "email": email, "password": password}
            response = await client.post(ADD_USER_URL, json=user_data)
            response_data = response.json()
            if response_data.get("status") == "error":
                return AddUserResponse(
                    status="error", message=response_data.get("message"), user=None
                )
            return AddUserResponse(
                status="success",
                message=response_data.get("message"),
                user=User(
                    username=response_data.get("username"),
                    email=response_data.get("email"),
                ),
            )
        except Exception as e:
            print(e)


async def update_user_password(user_id: int, old_password: str, new_password: str):
    from src.schema import UpdateUserResponse

    async with httpx.AsyncClient() as client:
        try:
            passwords = {"old_password": old_password, "new_password": new_password}
            url = UPDATE_PASSWORD_URL.format(user_id=user_id)
            response = await client.patch(url, json=passwords)
            response_data = response.json()
            return UpdateUserResponse(
                status=response_data.get("status"), message=response_data.get("message")
            )
        except Exception as e:
            print(e)


async def delete_user(self, user_id: int):
    from src.schema import DeleteUserResponse

    async with httpx.AsyncClient() as client:
        try:
            url = DELETE_USER_URL.format(user_id=user_id)
            response = await client.delete(url)
            response_data = response.json()
            return DeleteUserResponse(
                status=response_data.get("status"), message=response_data.get("message")
            )
        except Exception as e:
            print(e)

