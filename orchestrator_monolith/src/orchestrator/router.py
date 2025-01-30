from fastapi import APIRouter
from orchestrator_monolith.src.orchestrator.orchestrator import Orchestrator
from orchestrator_monolith.src.orchestrator.models import (
    SubscriptionRequest,
    ExtendSubscriptionRequest,
    UpdatePassword,
    User,
    UserIds,
    EmailList,
    ActivateRequest
)

fastapi_app = APIRouter(prefix="")

orchestrator = Orchestrator()

@fastapi_app.get("/get_subscriptions")
async def get_all_subscriptions():
    subscriptions = await orchestrator.get_all_subscriptions()    
    return {"subscriptions": subscriptions}

@fastapi_app.post("/add_subscription")
async def add_subscription(request: SubscriptionRequest):
    result = await orchestrator.add_subscription(request.email, request.subscription_type)
    return result

@fastapi_app.put("/extend_subscription/{email}")
async def extend_subscription(request: ExtendSubscriptionRequest):
    result = await orchestrator.extend_subscription(request.email, request.period)  
    return result

@fastapi_app.delete("/delete_subscription/{email}")
async def delete_subscription(email: str):
    result = await orchestrator.delete_subscription(email)
    return result

@fastapi_app.post("/activate_subscription/{email}")
async def activate_subscription(email: str, request: ActivateRequest):
    print(f"Received email: {email}, amount: {request.amount}")  # Debugging
    result = await orchestrator.activate_subscription(email, request.amount)
    return result

@fastapi_app.post("/deactivate_subscription/{email}")
async def deactivate_subscription(email: str):
    result = await orchestrator.deactivate_subscription(email)
    return result

@fastapi_app.get("/opt-out-policy")
async def opt_out_policy():
    policy_text = await orchestrator.get_opt_out_policy()
    return {"policy": policy_text}

@fastapi_app.get("/user_details/{user_id}")
async def get_user_details(user_id: int):
    result = await orchestrator.get_user(user_id=user_id)
    return result

@fastapi_app.post("/add_user")
async def add_user(user: User):
    result = await orchestrator.add_user(
        username=user.username, email=user.email, password=user.password
    )   
    return result

@fastapi_app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    result = await orchestrator.delete_user(user_id=user_id)
    return result

@fastapi_app.patch("/update_password/{user_id}")
async def update_password(user_id: int, passwords: UpdatePassword):
    result = await orchestrator.update_user_password(
        user_id=user_id,
        old_password=passwords.old_password,
        new_password=passwords.new_password,
    )
    return result


@fastapi_app.get("/get_user_id/{user_email}")
async def get_user_id_by_email(user_email: str):
    result = await orchestrator.get_user_id_by_email(email=user_email)
    return result

@fastapi_app.post("/users/emails")
async def get_users_emails_by_id(request: UserIds) -> EmailList:
    ids = request.ids
    result = await orchestrator.get_users_emails_by_id(ids)
    result_result = EmailList(**result)
    return result_result
