import httpx

async def fetch_data(url: str, method: str = "GET", data: dict = None):
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=data)
            elif method == "PATCH":
                response = await client.patch(url, json=data)
            elif method == "PUT":
                response = await client.put(url, json=data)
            elif method == "DELETE":
                response = await client.delete(url)
            else:
                raise ValueError("Unsupported HTTP method")
            return response.json()
        except Exception as e:
            print(f"Exception in fetch_data: {e}")
            return None


async def get_user_details(user_id: int):
    from graphql_service.graphql_app import User

    user_data = await fetch_data(f"http://localhost:5001/user_details/{user_id}")
    if not user_data:
        print("User not found.")
        return None
    return User(**user_data)


async def get_all_subscriptions_resolver():
    from graphql_service.graphql_app import Subscription
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:5001/get_subscriptions")
        raw_subscriptions = response.json().get("subscriptions", [])
        return [Subscription(**sub) for sub in raw_subscriptions]


async def opt_out_policy_resolver():
    from graphql_service.graphql_app import OptOutPolicyResponse

    policy_data = await fetch_data("http://localhost:5001/opt-out-policy")
    policy_text = policy_data.get("policy", "Unknown policy") if policy_data else "Unknown policy"
    return OptOutPolicyResponse(policy=policy_text)
