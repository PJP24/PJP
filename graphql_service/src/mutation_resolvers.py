import httpx
import os
from dotenv import load_dotenv
from strawberry.exceptions import GraphQLError
from strawberry.types import Info

load_dotenv()

BASE_URL = os.getenv("FASTAPI_BASE_URL")


def validate_subscription_type(subscription_type: str):
    if subscription_type not in ["monthly", "yearly"]:
        raise ValueError(
            "Only 'monthly' and 'yearly' are allowed as subscription types."
        )
    return subscription_type


async def add_subscription_resolver(email: str, subscription_type: str):
    from graphql_service.src.schema import AddSubscriptionResponse

    try:
        subscription_type = validate_subscription_type(subscription_type)
        url = f"{BASE_URL}/add_subscription"
        async with httpx.AsyncClient() as client:
            request = await client.post(
                url, json={"email": email, "subscription_type": subscription_type}
            )
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return AddSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error adding subscription: {e}")


async def extend_subscription_resolver(email: str, amount: int):
    from graphql_service.src.schema import ExtendSubscriptionResponse

    try:
        url = f"{BASE_URL}/extend_subscription/{email}?amount={amount}"
        async with httpx.AsyncClient() as client:
            request = await client.put(url)
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return ExtendSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error extending subscription: {e}")


async def delete_subscription_resolver(email: str):
    from graphql_service.src.schema import DeleteSubscriptionResponse

    try:
        url = f"{BASE_URL}/delete_subscription/{email}"
        async with httpx.AsyncClient() as client:
            request = await client.delete(url)
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return DeleteSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error deleting subscription: {e}")


async def activate_subscription_resolver(email: str, amount: int):
    from graphql_service.src.schema import ActivateSubscriptionResponse

    try:
        url = f"{BASE_URL}/activate_subscription/{email}"
        async with httpx.AsyncClient() as client:
            request = await client.post(url, json={"amount": amount})
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return ActivateSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error activating subscription: {e}")


async def deactivate_subscription_resolver(email: str):
    from graphql_service.src.schema import DeactivateSubscriptionResponse

    try:
        url = f"{BASE_URL}/deactivate_subscription/{email}"
        async with httpx.AsyncClient() as client:
            request = await client.post(url)
            request.raise_for_status()
            result_info = request.json().get("message", "Unknown result")
            return DeactivateSubscriptionResponse(result_info=result_info)
    except Exception as e:
        raise Exception(f"Error deactivating subscription: {e}")


async def add_user(username: str, email: str, password: str):
    from graphql_service.src.schema import AddUserResponse, CreatedUser

    user_data = {"username": username, "email": email, "password": password}
    url = f"{BASE_URL}/add_user"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=user_data)
            response.raise_for_status()
            response_data = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            return AddUserResponse(status="error", message=str(e), user=None)
        if response_data.get("status") == "error":
            return AddUserResponse(
                status="error", message=response_data.get("message"), user=None
            )
        return AddUserResponse(
            status="success",
            message=response_data.get("message"),
            user=CreatedUser(
                username=response_data.get("username"),
                email=response_data.get("email"),
                id=response_data.get("id"),
            ),
        )


async def update_user_password(
    user_id: int, old_password: str, new_password: str, info: Info
):
    from graphql_service.src.schema import Response

    token = info.context.get("token")
    if token is None:
        raise GraphQLError("Not authenticated.")

    passwords = {"old_password": old_password, "new_password": new_password}
    url = f"{BASE_URL}/update_password/{user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(url, json=passwords)
            response.raise_for_status()
            response_data = response.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            return Response(status="error", message=str(e))
        return Response(
            status=response_data.get("status"), message=response_data.get("message")
        )


async def delete_user(self, user_id: int, info: Info):
    from graphql_service.src.schema import Response

    token = info.context.get("token")
    if token is None:
        raise GraphQLError("Not authenticated.")

    url = f"{BASE_URL}/delete_user/{user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(url)
            response.raise_for_status()
            response_data = response.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            return Response(status="error", message=str(e))
        return Response(
            status=response_data.get("status"), message=response_data.get("message")
        )
