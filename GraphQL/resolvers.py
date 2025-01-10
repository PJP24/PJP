import httpx


async def get_all_subscriptions_resolver():
    from schema import Subscription
    async with httpx.AsyncClient() as client:
        response = await client.get("http://fastapi_service:8000/subscriptions")
        raw_subscriptions = response.json().get("subscriptions", [])
        return [Subscription(**sub) for sub in raw_subscriptions]

async def opt_out_policy_resolver() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://fastapi_service:8000/opt-out-policy")
        return response.json().get("policy", "Unknown policy")


async def add_subscription_resolver(email: str, subscription_type: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://fastapi_service:8000/subscriptions",
            json={"email": email, "subscription_type": subscription_type},
        )
        return response.json().get("message", "Unknown result")

async def change_subscription_resolver(email: str, subscription_type: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.put(
            "http://fastapi_service:8000/subscriptions",
            json={"email": email, "subscription_type": subscription_type},
        )
        return response.json().get("message", "Unknown result")

async def delete_subscription_resolver(email: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"http://fastapi_service:8000/subscriptions/{email}",
        )
        return response.json().get("message", "Unknown result")

async def activate_subscription_resolver(email: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://fastapi_service:8000/subscriptions/{email}/activate",
        )
        return response.json().get("message", "Unknown result")

async def deactivate_subscription_resolver(email: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://fastapi_service:8000/subscriptions/{email}/deactivate",
        )
        return response.json().get("message", "Unknown result")
