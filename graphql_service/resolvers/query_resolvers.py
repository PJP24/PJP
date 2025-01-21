import httpx
from typing import Optional, Dict, Any

async def fetch_data(url: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, json=data)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except httpx.RequestError as e:
            print(f"Request error: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP status error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

async def get_user_details(user_id: int):
    from graphql_service.graphql_app import User
    user_data = await fetch_data(f"http://fastapi_orchestrator:5001/user_details/{user_id}")
    if not user_data:
        print("User not found.")
        return None
    return User(**user_data)

async def get_all_subscriptions_resolver():
    from graphql_service.graphql_app import Subscription
    try:
        url = "http://fastapi_orchestrator:5001/get_subscriptions"
        async with httpx.AsyncClient() as client:
            request = await client.get(url)
            request.raise_for_status()
            raw_subscriptions = request.json().get("subscriptions", [])
            return [Subscription(**sub) for sub in raw_subscriptions]
    except Exception as e:
        raise Exception(f"Error fetching subscriptions: {e}")


async def opt_out_policy_resolver():
    from graphql_service.graphql_app import OptOutPolicyResponse
    try:
        url = "http://fastapi_orchestrator:5001/opt-out-policy"
        async with httpx.AsyncClient() as client:
            request = await client.get(url)
            request.raise_for_status()
            policy_text = request.json().get("policy", "Unknown policy")
            return OptOutPolicyResponse(policy=policy_text)
    except Exception as e:
        raise Exception(f"Error fetching opt-out policy: {e}")


