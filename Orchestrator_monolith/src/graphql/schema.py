import strawberry
from src.orchestrator.orchestrator import Orchestrator
from typing import Optional
from typing import List

@strawberry.type
class Subscription:
    email: str
    subscription_type: str

@strawberry.type
class User:
    user_id: str
    name: str
    email: str

@strawberry.type
class AddUserResponse:
    status: str
    message: str
    user: Optional[User]

@strawberry.type
class UpdateUserResponse:
    status: str
    message: str
    user: Optional[User]

@strawberry.type
class DeleteUserResponse:
    status: str
    message: str
    user_id: Optional[str]

@strawberry.type
class AddSubscriptionResponse:
    status: str

@strawberry.type
class UpdateSubscriptionResponse:
    status: str

@strawberry.type
class Query:
    @strawberry.field
    async def get_user_details(self, user_id: str) -> Optional[User]:
        try:
            orchestrator = Orchestrator()
            user_data = await orchestrator.get_user(user_id)
            if "error" in user_data:
                print(f"Error fetching user details: {user_data['error']}")
                return None
            return User(**user_data)
        except Exception as e:
            print(f"Exception in get_user_details: {e}")
            return None
    
    @strawberry.field
    async def get_all_subscriptions(self) -> List[Subscription]:
        try:
            orchestrator = Orchestrator()
            subscriptions = await orchestrator.get_all_subscriptions()
            return subscriptions
        except Exception as e:
            print(f"Exception: {e}")
            return []

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_user(self, name: str, email: str) -> AddUserResponse:
        orchestrator = Orchestrator()
        user_data = await orchestrator.add_user(name, email)

        if "error" in user_data:
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

    @strawberry.mutation
    async def update_user(self, user_id: str, name: str, email: str) -> UpdateUserResponse:
        orchestrator = Orchestrator()
        user_data = await orchestrator.update_user(user_id, name, email)

        if "error" in user_data:
            return UpdateUserResponse(
                status="error",
                message=user_data.get("error", "An error occurred"),
                user=None
            )
        return UpdateUserResponse(
            status="success",
            message="User successfully updated",
            user=User(**user_data)
        )

    @strawberry.mutation
    async def delete_user(self, user_id: str) -> DeleteUserResponse:
        orchestrator = Orchestrator()
        user_data = await orchestrator.delete_user(user_id)

        if "error" in user_data:
            return DeleteUserResponse(
                status="error",
                message=user_data.get("error", "An error occurred"),
                user_id=None
            )
        return DeleteUserResponse(
            status="success",
            message="User successfully deleted",
            user_id=user_id
        )

    @strawberry.mutation
    async def add_subscription(self, email: str, subscription_type: str) -> AddSubscriptionResponse:
        orchestrator = Orchestrator()
        subscription_data = await orchestrator.add_subscription(email, subscription_type)

        if "error" in subscription_data:
            return AddSubscriptionResponse(
                status="error",
            )
        return AddSubscriptionResponse(
            status="success",
        )
    
    @strawberry.mutation
    async def change_subscription(self, email: str, subscription_type: str) -> UpdateSubscriptionResponse:
        orchestrator = Orchestrator()
        subscription_data = await orchestrator.change_subscription(email, subscription_type)

        if "error" in subscription_data:
            return AddSubscriptionResponse(
                status="error",
            )
        return AddSubscriptionResponse(
            status="success",
        )
