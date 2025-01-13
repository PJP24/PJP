import strawberry
from typing import List, Optional
from strawberry.fastapi import GraphQLRouter
from graphql_service.resolvers.query_resolvers import get_user_details, get_all_subscriptions_resolver, opt_out_policy_resolver
from graphql_service.resolvers.mutation_resolvers import (
    add_user,
    add_subscription_resolver,
    change_subscription_resolver,
    delete_subscription_resolver,
    activate_subscription_resolver,
    deactivate_subscription_resolver,
    update_user_password,
    delete_user,
)

@strawberry.type
class User:
    username: str | None
    email: str | None


@strawberry.type
@strawberry.type
class Subscription:
    email: str | None
    subscription_type: str | None
    is_active: str | None


@strawberry.type
class AddUserResponse:
    status: str | None
    message: str | None
    user: Optional[User] | None


@strawberry.type
class UpdateUserResponse:
    status: str | None
    message: str | None


@strawberry.type
class AddSubscriptionResponse:
    status: str | None
    message: str | None
    subscription: Optional[Subscription] | None


@strawberry.type
class DeleteUserResponse:
    status: str | None
    message: str | None


@strawberry.type
class OptOutPolicyResponse:
    policy: str | None


@strawberry.type
class AddSubscriptionResponse:
    result_info: str | None


@strawberry.type
class UpdateSubscriptionResponse:
    result_info: str | None


@strawberry.type
class DeleteSubscriptionResponse:
    result_info: str | None


@strawberry.type
class ActivateSubscriptionResponse:
    result_info: str | None


@strawberry.type
class DeactivateSubscriptionResponse:
    result_info: str | None


@strawberry.type
class Query:
    user_details: User | None = strawberry.field(resolver=get_user_details)
    all_subscriptions: List[Subscription | None] = strawberry.field(resolver=get_all_subscriptions_resolver)
    opt_out_policy: OptOutPolicyResponse | None = strawberry.field(resolver=opt_out_policy_resolver)


@strawberry.type
class Mutation:
    add_user: AddUserResponse | None = strawberry.field(resolver=add_user)
    update_user_password: UpdateUserResponse | None = strawberry.field(resolver=update_user_password)
    delete_user: DeleteUserResponse | None = strawberry.field(resolver=delete_user)
    add_subscription: AddSubscriptionResponse | None = strawberry.field(resolver=add_subscription_resolver)
    change_subscription: UpdateSubscriptionResponse | None = strawberry.field(resolver=change_subscription_resolver)
    delete_subscription: DeleteSubscriptionResponse | None = strawberry.field(resolver=delete_subscription_resolver)
    activate_subscription: ActivateSubscriptionResponse | None = strawberry.field(resolver=activate_subscription_resolver)
    deactivate_subscription: DeactivateSubscriptionResponse | None = strawberry.field(resolver=deactivate_subscription_resolver)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)
