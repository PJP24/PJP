<<<<<<< HEAD
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
=======

# import strawberry
# from typing import List
# import requests


# @strawberry.type
# class Subscription:
#     email: str
#     subscription_type: str
#     is_active: str

import strawberry
from typing import Optional
import requests



@strawberry.type
class User:
    username: str
    email: str





# @strawberry.type
# class Query:
#     @strawberry.field
#     def get_all_subscriptions(self) -> List[Subscription]:
#         response = requests.get("http://fastapi_service:8000/subscriptions")
#         subscriptions = response.json().get("subscriptions", [])
#         return [Subscription(**sub) for sub in subscriptions]
>>>>>>> e50b996 (Separate graphql from orchestrator)


@strawberry.type
class Subscription:
<<<<<<< HEAD
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
=======
    user_id: int
    period: str
    subscription_type: str


@strawberry.type
class AddUserResponse:
    status: str
    message: str
    user: Optional[User]


@strawberry.type
class UpdateUserResponse:
    status: str
    message: str



# @strawberry.type
# class AddSubscriptionResponse:
#     result_info: str

# @strawberry.type
# class UpdateSubscriptionResponse:
#     result_info: str


# @strawberry.type
# class DeleteSubscriptionResponse:
#     result_info: str

# @strawberry.type
# class ActivateSubscriptionResponse:
#     result_info: str


@strawberry.type
class DeleteUserResponse:
    status: str
    message: str


@strawberry.type
class Query:
    @strawberry.field
    async def get_user_details(self, user_id: int) -> Optional[User]:
        try:
            print("test")
            response = requests.get(f"http://fast-api:8000/users/user_details/{user_id}")
            print(response)
            user_data = response.json()
            if user_data is None:
                print("User not found.")
                return None
            return User(**user_data)
        except Exception as e:
            print(f"Exception in get_user_details: {e}")
            return None



# @strawberry.type
# class DeactivateSubscriptionResponse:
#     result_info: str

# @strawberry.type
# class OptOutPolicyResponse:
#     policy: str

# @strawberry.type
# class Mutation:
#     @strawberry.mutation
#     async def add_subscription(self, email: str, subscription_type: str) -> AddSubscriptionResponse:
#         response = requests.post(
#             "http://fastapi_service:8000/subscriptions",
#             json={"email": email, "subscription_type": subscription_type},
#         )
#         result_info = response.json().get("message", "Unknown result")
#         return AddSubscriptionResponse(result_info=result_info)
=======
        except Exception as e:
            print(f"Exception in get_user_details: {e}")
            return None
>>>>>>> 7244560 (Add FastAPI for orchestrator)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_user(
        self, username: str, email: str, password: str
    ) -> AddUserResponse:
        try:
            user_data = {"username": username, "email": email, "password": password}
            response = requests.post("http://fast-api:8000/users/add_user", json=user_data)
            response_data = response.json()
            if response_data.get("status") == "error":
                return AddUserResponse(
                    status="error", message=response_data.get("message"), user=None
                )
            return AddUserResponse(
                status="success",
                message=response_data.get("message"),
                user=User(
                    username=response_data.get("username"),
                    email=response_data.get("email"),
                ),
            )
        except Exception as e:
            print(e)



#     @strawberry.mutation
#     async def activate_subscription(self, email: str) -> ActivateSubscriptionResponse:
#         response = requests.post(f"http://fastapi_service:8000/subscriptions/{email}/activate")
#         result_info = response.json().get("message", "Unknown result")
#         return ActivateSubscriptionResponse(result_info=result_info)

    @strawberry.mutation

    async def update_user_password(self, user_id: int, old_password: str, new_password: str) -> UpdateUserResponse:
        orchestrator = Orchestrator()
        response = await orchestrator.update_user_password(user_id, old_password, new_password)
        print(response)
        return UpdateUserResponse(
            status=response.status,
            message=response.message,
        )


#     @strawberry.mutation
#     async def deactivate_subscription(self, email: str) -> DeactivateSubscriptionResponse:
#         response = requests.post(f"http://fastapi_service:8000/subscriptions/{email}/deactivate")
#         result_info = response.json().get("message", "Unknown result")
#         return DeactivateSubscriptionResponse(result_info=result_info)


#     @strawberry.mutation
#     async def opt_out_policy(self) -> OptOutPolicyResponse:
#         response = requests.get("http://fastapi_service:8000/opt-out-policy")
#         policy = response.json().get("policy", "No policy available")
#         return OptOutPolicyResponse(policy=policy)

        if "error" in subscription_data:
            return AddSubscriptionResponse(
                status="error",
                message=subscription_data.get("error", "An error occurred"),
                subscription=None
    async def update_user_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> UpdateUserResponse:
        try:
            passwords = {"old_password": old_password, "new_password": new_password}
            response = requests.patch(
                f"http://fast-api:8000/users/update_password/{user_id}", json=passwords
            )
            response_data = response.json()
            print(response_data)
            return UpdateUserResponse(
                status=response_data.get("status"), message=response_data.get("message")
            )
        except Exception as e:
            print(e)

    @strawberry.mutation

    async def delete_user(self, user_id: int, confirmation: bool) -> DeleteUserResponse:
        orchestrator = Orchestrator()
        user_data = await orchestrator.delete_user(user_id, confirmation)
        return DeleteUserResponse(
            status=user_data.get("status", "Unknown"),
            message=user_data.get("message", "Unknown message"),
        )


    async def delete_user(self, user_id: int) -> DeleteUserResponse:
        try:
            response = requests.delete(f"http://fast-api:8000/users/delete_user/{user_id}")
            response_data = response.json()
            return DeleteUserResponse(
                status=response_data.get("status"), message=response_data.get("message")
            )
        except Exception as e:
            print(e)

>>>>>>> e50b996 (Separate graphql from orchestrator)
