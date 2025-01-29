import strawberry
from typing import List, Optional

from graphql_service.src.query_resolvers import (
    get_all_subscriptions_resolver,
    opt_out_policy_resolver,
    get_user_details,
)
from graphql_service.src.mutation_resolvers import (
    add_subscription_resolver,
    extend_subscription_resolver,
    delete_subscription_resolver,
    activate_subscription_resolver,
    deactivate_subscription_resolver,
    add_user,
    update_user_password,
    delete_user,
    pay_subscription_resolver
)

@strawberry.type
class Subscription:
    id: str
    is_active: str
    end_date: str
    user_id: str

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
class PaySubscriptionResponse:
    status: str
    message: str

@strawberry.type
class User:
    username: str
    email: str

@strawberry.type
class CreatedUser:
    username: str
    email: str
    id: int


@strawberry.type
class AddUserResponse:
    status: str
    message: str
    user: Optional[CreatedUser]

@strawberry.type
class Response:
    status: str
    message: str


@strawberry.type
class Query:
    all_subscriptions: List[Subscription] | None = strawberry.field(resolver=get_all_subscriptions_resolver)
    opt_out_policy: OptOutPolicyResponse | None = strawberry.field(resolver=opt_out_policy_resolver)
    user_details: User | None = strawberry.field(resolver=get_user_details)

@strawberry.type
class Mutation:
    add_subscription: AddSubscriptionResponse | None = strawberry.field(resolver=add_subscription_resolver)
    extend_subscription: UpdateSubscriptionResponse | None = strawberry.field(resolver=extend_subscription_resolver)
    delete_subscription: DeleteSubscriptionResponse | None = strawberry.field(resolver=delete_subscription_resolver)
    activate_subscription: ActivateSubscriptionResponse | None = strawberry.field(
        resolver=activate_subscription_resolver)
    deactivate_subscription: DeactivateSubscriptionResponse | None = strawberry.field(
        resolver=deactivate_subscription_resolver)
    create_user: AddUserResponse | None = strawberry.field(resolver=add_user)
    delete_user: Response | None = strawberry.field(resolver=delete_user)
    update_password: Response | None = strawberry.field(resolver=update_user_password)
    pay_subscription: PaySubscriptionResponse | None = strawberry.field(resolver=pay_subscription_resolver)