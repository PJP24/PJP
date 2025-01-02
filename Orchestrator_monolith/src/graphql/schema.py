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
    # user_id: str
    username: str
    email: str


# @strawberry.type
# class Query:
#     @strawberry.field
#     def get_all_subscriptions(self) -> List[Subscription]:
#         response = requests.get("http://fastapi_service:8000/subscriptions")
#         subscriptions = response.json().get("subscriptions", [])
#         return [Subscription(**sub) for sub in subscriptions]

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

        if "error" in user_data:
            print(user_data)
            return AddUserResponse(
                status="error",
                message=user_data.get("error", "An error occurred"),
                user=None
            )
        return AddUserResponse(
            status="success",
            message="User successfully added",
            user=User(**user_data)
        )


#     @strawberry.mutation
#     async def activate_subscription(self, email: str) -> ActivateSubscriptionResponse:
#         response = requests.post(f"http://fastapi_service:8000/subscriptions/{email}/activate")
#         result_info = response.json().get("message", "Unknown result")
#         return ActivateSubscriptionResponse(result_info=result_info)

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
