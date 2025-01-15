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
class OptOutPolicyResponse:
    policy: str
    
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
class Query:
    all_subscriptions: List[Subscription] = strawberry.field(resolver=get_all_subscriptions_resolver)
    opt_out_policy: OptOutPolicyResponse = strawberry.field(resolver=opt_out_policy_resolver)

@strawberry.type
class Mutation:
    add_subscription: AddSubscriptionResponse = strawberry.field(resolver=add_subscription_resolver)
    change_subscription: UpdateSubscriptionResponse = strawberry.field(resolver=change_subscription_resolver)
    delete_subscription: DeleteSubscriptionResponse = strawberry.field(resolver=delete_subscription_resolver)
    activate_subscription: ActivateSubscriptionResponse = strawberry.field(resolver=activate_subscription_resolver)
    deactivate_subscription: DeactivateSubscriptionResponse = strawberry.field(resolver=deactivate_subscription_resolver)
