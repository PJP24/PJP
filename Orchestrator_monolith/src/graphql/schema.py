# import strawberry
# from typing import List
# import requests


# @strawberry.type
# class Subscription:
#     email: str
#     subscription_type: str
#     is_active: str

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

@strawberry.type
class Subscription:
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
            orchestrator = Orchestrator()
            user_data = await orchestrator.get_user(user_id)
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


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_user(self, username: str, email: str, password: str) -> AddUserResponse:
        orchestrator = Orchestrator()
        user_data = await orchestrator.add_user(username=username, email=email, password=password)
        print(user_data.status)

        if user_data.status == "error":
            return AddUserResponse(
                status="error",
                message=user_data.message,
                user=None
            )
        return AddUserResponse(
            status="success",
            message=user_data.message,
            user=User(username=user_data.username, email=user_data.email)
        )



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
            )
        return AddSubscriptionResponse(
            status="success",
            message="Subscription successfully added",
            subscription=Subscription(**subscription_data)
        )

    @strawberry.mutation
    async def delete_user(self, user_id: int, confirmation: bool) -> DeleteUserResponse:
        orchestrator = Orchestrator()
        user_data = await orchestrator.delete_user(user_id, confirmation)
        return DeleteUserResponse(
            status=user_data.get("status", "Unknown"),
            message=user_data.get("message", "Unknown message"),
        )

