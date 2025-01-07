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
    result_info: str

@strawberry.type
class UpdateSubscriptionResponse:
    result_info: str

@strawberry.type
class DeleteSubscriptionResponse:
    result_info: str

@strawberry.type
class ActivateSubscriptionResponse:
    result_info: str

@strawberry.type
class DeactivateSubscriptionResponse:
    result_info: str

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
            return AddSubscriptionResponse(result_info="A subscription with this email already exists.")

        response = requests.post("http://fastapi_service:8000/subscriptions", json={"email": email, "subscription_type": subscription_type})
        return AddSubscriptionResponse(result_info="Subscription successfully added." if response.status_code == 200 else "Failed to add subscription.")

    @strawberry.mutation
    async def change_subscription(self, email: str, subscription_type: str) -> UpdateSubscriptionResponse:
        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])

        subscription = next((s for s in subscriptions if s["email"] == email), None)

        if not subscription:
            return UpdateSubscriptionResponse(result_info="Subscription with this email doesn't exist.")

        if subscription["subscription_type"] == subscription_type:
            return UpdateSubscriptionResponse(result_info=f"Subscription is already {subscription_type}.")

        response = requests.put("http://fastapi_service:8000/subscriptions", json={"email": email, "subscription_type": subscription_type})
        return UpdateSubscriptionResponse(result_info="Subscription successfully updated." if response.status_code == 200 else "Failed to update subscription.")

    @strawberry.mutation
    async def delete_subscription(self, email: str) -> DeleteSubscriptionResponse:
        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])

        if not any(subscription["email"] == email for subscription in subscriptions):
            return DeleteSubscriptionResponse(result_info="Subscription with this email doesn't exist.")

        response = requests.delete(f"http://fastapi_service:8000/subscriptions/{email}")
        return DeleteSubscriptionResponse(result_info="Subscription successfully deleted." if response.status_code == 200 else "Failed to delete subscription.")

    @strawberry.mutation
    async def activate_subscription(self, email: str) -> ActivateSubscriptionResponse:
        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])
        
        subscription = next((s for s in subscriptions if s["email"] == email), None)

        if not subscription:
            return ActivateSubscriptionResponse(result_info="Subscription with this email doesn't exist.")

        if subscription["is_active"]:
            return ActivateSubscriptionResponse(result_info="Subscription with this email is already active.")
        
        response = requests.post(f"http://fastapi_service:8000/subscriptions/{email}/activate")
        return ActivateSubscriptionResponse(result_info="Subscription successfully activated." if response.status_code == 200 else "Failed to activate subscription.")

    @strawberry.mutation
    async def deactivate_subscription(self, email: str) -> DeactivateSubscriptionResponse:
        response = requests.get("http://fastapi_service:8000/subscriptions")
        subscriptions = response.json().get("subscriptions", [])
        
        subscription = next((s for s in subscriptions if s["email"] == email), None)

        if not subscription:
            return DeactivateSubscriptionResponse(result_info="Subscription with this email doesn't exist.")
        
        if not subscription["is_active"]:
            return DeactivateSubscriptionResponse(result_info="Subscription with this email is already inactive.")
        
        response = requests.post(f"http://fastapi_service:8000/subscriptions/{email}/deactivate")
        return DeactivateSubscriptionResponse(result_info="Subscription successfully deactivated." if response.status_code == 200 else "Failed to deactivate subscription.")

    @strawberry.mutation
    async def opt_out_policy(self) -> OptOutPolicyResponse:
        response = requests.get("http://fastapi_service:8000/opt-out-policy")
        if response.status_code == 200:
            policy_text = response.json().get("policy", "No policy available")
            return OptOutPolicyResponse(policy=policy_text)
        return OptOutPolicyResponse(policy="Error fetching policy")
