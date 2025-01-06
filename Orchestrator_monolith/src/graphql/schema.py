import strawberry
from typing import List
from src.orchestrator.orchestrator import Orchestrator

@strawberry.type
class Subscription:
    email: str
    subscription_type: str
    is_active: str

@strawberry.type
class Query:
    @strawberry.field
    async def get_all_subscriptions(self) -> List[Subscription]:
        orchestrator = Orchestrator()
        subscriptions = await orchestrator.get_all_subscriptions()
        return subscriptions

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
        orchestrator = Orchestrator()
        subscription_data = await orchestrator.add_subscription(email, subscription_type)
        if "error" in subscription_data:
            return AddSubscriptionResponse(status="error")
        return AddSubscriptionResponse(status="success")
    
    @strawberry.mutation
    async def change_subscription(self, email: str, subscription_type: str) -> UpdateSubscriptionResponse:
        orchestrator = Orchestrator()
        subscription_data = await orchestrator.change_subscription(email, subscription_type)
        if "error" in subscription_data:
            return UpdateSubscriptionResponse(status="error")
        return UpdateSubscriptionResponse(status="success")

    @strawberry.mutation
    async def delete_subscription(self, email: str) -> DeleteSubscriptionResponse:
        orchestrator = Orchestrator()
        subscription_data = await orchestrator.delete_subscription(email)
        if "error" in subscription_data:
            return DeleteSubscriptionResponse(status="error")
        return DeleteSubscriptionResponse(status="success")

    @strawberry.mutation
    async def activate_subscription(self, email: str) -> ActivateSubscriptionResponse:
        orchestrator = Orchestrator()
        await orchestrator.activate_subscription(email)
        return ActivateSubscriptionResponse(status="success")

    @strawberry.mutation
    async def deactivate_subscription(self, email: str) -> DeactivateSubscriptionResponse:
        orchestrator = Orchestrator()
        await orchestrator.deactivate_subscription(email)
        return DeactivateSubscriptionResponse(status="success")

    @strawberry.mutation
    async def opt_out_policy(self) -> OptOutPolicyResponse:
        orchestrator = Orchestrator()
        policy_text = await orchestrator.get_opt_out_policy()
        return OptOutPolicyResponse(policy=policy_text)
