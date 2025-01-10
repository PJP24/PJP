import strawberry
from typing import List
from resolvers import (
    get_all_subscriptions_resolver,
    add_subscription_resolver,
    change_subscription_resolver,
    delete_subscription_resolver,
    activate_subscription_resolver,
    deactivate_subscription_resolver,
    opt_out_policy_resolver,
)

@strawberry.type
class Subscription:
    email: str
    subscription_type: str
    is_active: str

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
class Query:
    @strawberry.field(resolver=get_all_subscriptions_resolver)
    def all_subscriptions(self) -> List[Subscription]:
        print("Get all subscriptions.")
        return get_all_subscriptions_resolver()

    @strawberry.mutation(resolver=opt_out_policy_resolver)
    def opt_out_policy(self) -> OptOutPolicyResponse:
        policy = opt_out_policy_resolver()
        return OptOutPolicyResponse(policy=policy)
    
@strawberry.type
class Mutation:
    @strawberry.mutation(resolver=add_subscription_resolver)
    def add_subscription(self, email: str, subscription_type: str) -> AddSubscriptionResponse:
        print("Add subscription.")
        result_info = add_subscription_resolver(email, subscription_type)
        return AddSubscriptionResponse(result_info=result_info)

    @strawberry.mutation(resolver=change_subscription_resolver)
    def change_subscription(self, email: str, subscription_type: str) -> UpdateSubscriptionResponse:
        result_info = change_subscription_resolver(email, subscription_type)
        return UpdateSubscriptionResponse(result_info=result_info)

    @strawberry.mutation(resolver=delete_subscription_resolver)
    def delete_subscription(self, email: str) -> DeleteSubscriptionResponse:
        result_info = delete_subscription_resolver(email)
        return DeleteSubscriptionResponse(result_info=result_info)

    @strawberry.mutation(resolver=activate_subscription_resolver)
    def activate_subscription(self, email: str) -> ActivateSubscriptionResponse:
        result_info = activate_subscription_resolver(email)
        return ActivateSubscriptionResponse(result_info=result_info)

    @strawberry.mutation(resolver=deactivate_subscription_resolver)
    def deactivate_subscription(self, email: str) -> DeactivateSubscriptionResponse:
        result_info = deactivate_subscription_resolver(email)
        return DeactivateSubscriptionResponse(result_info=result_info)
