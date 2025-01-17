import strawberry
from typing import List

from src.querry_resolvers import (
    get_all_subscriptions_resolver,
    opt_out_policy_resolver,
)

from src.mutation_resolvers import (
    add_subscription_resolver,
    extend_subscription_resolver,
    delete_subscription_resolver,
    activate_subscription_resolver,
    deactivate_subscription_resolver,
)


@strawberry.type
class Subscription:
    email: str
    subscription_type: str
    is_active: str
    end_date: str

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
class ExtendSubscriptionResponse:
    result_info: str

@strawberry.type
class Query:
    all_subscriptions: List[Subscription] | None = strawberry.field(resolver=get_all_subscriptions_resolver)
    opt_out_policy: OptOutPolicyResponse | None = strawberry.field(resolver=opt_out_policy_resolver)

@strawberry.type
class Mutation:
    add_subscription: AddSubscriptionResponse | None = strawberry.field(resolver=add_subscription_resolver)
    extend_subscription: UpdateSubscriptionResponse | None = strawberry.field(resolver=extend_subscription_resolver)
    delete_subscription: DeleteSubscriptionResponse | None = strawberry.field(resolver=delete_subscription_resolver)
    activate_subscription: ActivateSubscriptionResponse | None = strawberry.field(resolver=activate_subscription_resolver)
    deactivate_subscription: DeactivateSubscriptionResponse | None = strawberry.field(resolver=deactivate_subscription_resolver)
