import strawberry
from typing import List
import requests

@strawberry.type
class Subscription:
    email: str
    subscription_type: str
    is_active: str

@strawberry.type
class Query:
    @strawberry.field
    def get_all_subscriptions(self) -> List[Subscription]:
        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])
        return [Subscription(**sub) for sub in subscriptions]

@strawberry.type
class AddSubscriptionResponse:
    status: str

@strawberry.type
class UpdateSubscriptionResponse:
    status: str

@strawberry.type
class DeleteSubscriptionResponse:
    status: str

@strawberry.type
class ActivateSubscriptionResponse:
    status: str

@strawberry.type
class DeactivateSubscriptionResponse:
    status: str

@strawberry.type
class OptOutPolicyResponse:
    policy: str

@strawberry.type
class Mutation:


    @strawberry.mutation
    async def add_subscription(self, email: str, subscription_type: str) -> AddSubscriptionResponse:
        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])

        if any(subscription["email"] == email for subscription in subscriptions):
            return AddSubscriptionResponse(status="Subscription with this email already exists.")

        response = requests.post("http://fastapi_service:8000/subscriptions", json={"email": email, "subscription_type": subscription_type})
        return AddSubscriptionResponse(status="success" if response.status_code == 200 else "error")


    @strawberry.mutation
    async def change_subscription(self, email: str, subscription_type: str) -> UpdateSubscriptionResponse:
        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])

        subscription = next((s for s in subscriptions if s["email"] == email), None)

        if not subscription:
            return UpdateSubscriptionResponse(status="Subscription with this email doesn't exist.")

        if subscription["subscription_type"] == subscription_type:
            return UpdateSubscriptionResponse(status=f"Subscription is already {subscription_type}.")

        response = requests.put("http://fastapi_service:8000/subscriptions", json={"email": email, "subscription_type": subscription_type})
        return UpdateSubscriptionResponse(status="success" if response.status_code == 200 else "error")


    @strawberry.mutation
    async def delete_subscription(self, email: str) -> DeleteSubscriptionResponse:
        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])

        if not any(subscription["email"] == email for subscription in subscriptions):
            return DeleteSubscriptionResponse(status="Subscription with this email doesn't exist.")

        response = requests.delete(f"http://fastapi_service:8000/subscriptions/{email}")
        return DeleteSubscriptionResponse(status="success" if response.status_code == 200 else "error")

    @strawberry.mutation
    async def activate_subscription(self, email: str) -> ActivateSubscriptionResponse:

        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])
        
        subscription = next((s for s in subscriptions if s["email"] == email), None)

        if not any(subscription["email"] == email for subscription in subscriptions):
            return ActivateSubscriptionResponse(status="Subscription with this email doesn't exist.")

        if subscription["is_active"]:
            return ActivateSubscriptionResponse(status="Subscription with this email is already active.")
        
        response = requests.post(f"http://fastapi_service:8000/subscriptions/{email}/activate")
        if response.status_code == 200:
            return ActivateSubscriptionResponse(status="success")
        return ActivateSubscriptionResponse(status="error")

    @strawberry.mutation
    async def deactivate_subscription(self, email: str) -> DeactivateSubscriptionResponse:
        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])
        
        subscription = next((s for s in subscriptions if s["email"] == email), None)

        if not subscription:
            return DeactivateSubscriptionResponse(status="Subscription with this email doesn't exist.")
        
        if not subscription["is_active"]:
            return DeactivateSubscriptionResponse(status="Subscription with this email is already inactive.")
        
        response = requests.post(f"http://fastapi_service:8000/subscriptions/{email}/deactivate")
        if response.status_code == 200:
            return DeactivateSubscriptionResponse(status="success")
        return DeactivateSubscriptionResponse(status="error")

    @strawberry.mutation
    async def opt_out_policy(self) -> OptOutPolicyResponse:
        response = requests.get("http://fastapi_service:8000/opt-out-policy")
        if response.status_code == 200:
            policy_text = response.json().get("policy", "No policy available")
            return OptOutPolicyResponse(policy=policy_text)
        return OptOutPolicyResponse(policy="Error fetching policy")
