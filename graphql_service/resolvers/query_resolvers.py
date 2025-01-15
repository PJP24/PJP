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
    subscriptions_data = await fetch_data("http://fastapi_orchestrator:5001/get_subscriptions")
    if not subscriptions_data or "subscriptions" not in subscriptions_data:
        print("No subscriptions found.")
        return []
    raw_subscriptions = subscriptions_data["subscriptions"]
    return [Subscription(**sub) for sub in raw_subscriptions]

async def opt_out_policy_resolver():
    from graphql_service.graphql_app import OptOutPolicyResponse
    policy_data = await fetch_data("http://fastapi_orchestrator:5001/opt-out-policy")
    policy_text = policy_data.get("policy", "Unknown policy") if policy_data else "Unknown policy"
    return OptOutPolicyResponse(policy=policy_text)
