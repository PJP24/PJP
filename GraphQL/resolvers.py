import httpx

async def get_all_subscriptions_resolver():
    from schema import Subscription
    async with httpx.AsyncClient() as client:
        response = await client.get("http://fastapi_service:8000/subscriptions")
        raw_subscriptions = response.json().get("subscriptions", [])
        return [Subscription(**sub) for sub in raw_subscriptions]

async def opt_out_policy_resolver():
    from schema import OptOutPolicyResponse
    async with httpx.AsyncClient() as client:
        response = await client.get("http://fastapi_service:8000/opt-out-policy")
        policy_text = response.json().get("policy", "Unknown policy")
        return OptOutPolicyResponse(policy=policy_text)

async def add_subscription_resolver(email: str, subscription_type: str):
    from schema import AddSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://fastapi_service:8000/subscriptions",
            json={"email": email, "subscription_type": subscription_type},
        )
        result_info = response.json().get("message", "Unknown result")
        return AddSubscriptionResponse(result_info=result_info)

async def change_subscription_resolver(email: str, subscription_type: str):
    from schema import UpdateSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.put(
            "http://fastapi_service:8000/subscriptions",
            json={"email": email, "subscription_type": subscription_type},
        )
        result_info = response.json().get("message", "Unknown result")
        return UpdateSubscriptionResponse(result_info=result_info)

async def delete_subscription_resolver(email: str):
    from schema import DeleteSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"http://fastapi_service:8000/subscriptions/{email}",
        )
        result_info = response.json().get("message", "Unknown result")
        return DeleteSubscriptionResponse(result_info=result_info)

async def activate_subscription_resolver(email: str):
    from schema import ActivateSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://fastapi_service:8000/subscriptions/{email}/activate",
        )
        result_info = response.json().get("message", "Unknown result")
        return ActivateSubscriptionResponse(result_info=result_info)

async def deactivate_subscription_resolver(email: str):
    from schema import DeactivateSubscriptionResponse
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://fastapi_service:8000/subscriptions/{email}/deactivate",
        )
        result_info = response.json().get("message", "Unknown result")
        return DeactivateSubscriptionResponse(result_info=result_info)
