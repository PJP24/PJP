from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse, HTMLResponse
from orchestrator_monolith.src.orchestrator.orchestrator import Orchestrator
from orchestrator_monolith.src.orchestrator.models import SubscriptionRequest, ExtendSubscriptionRequest, UpdatePassword, User, UserIds, EmailList, Payment

from orchestrator_monolith.src.orchestrator.models import (
    SubscriptionRequest,
    ExtendSubscriptionRequest,
    UpdatePassword,
    User,
    UserIds,
    EmailList,
    ActivateRequest
)

from orchestrator_monolith.src.orchestrator.oauth import google, github

fastapi_app = APIRouter(prefix="")

orchestrator = Orchestrator()


@fastapi_app.get("/login")
async def login(request: Request):
    return HTMLResponse(
        """
        <p>Please choose which to use for authenticating:</p>
        <a href='/login/google'> Google </a>
        <br>
        <a href='/login/github'> Github </a>
        """
    )


@fastapi_app.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_callback_google")
    return await google.authorize_redirect(request, redirect_uri)

@fastapi_app.get("/login/github")
async def login_github(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await github.authorize_redirect(request, redirect_uri)

@fastapi_app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await github.authorize_access_token(request)
    user_info = await github.get("user", token=token)
    user = user_info.json()
    if user:
        request.session['user'] = dict(user)
    print(user)
    return RedirectResponse(url='/docs')


@fastapi_app.get("/auth/callback/google")
async def auth_callback_google(request: Request):
    token = await google.authorize_access_token(request)
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/docs')

@fastapi_app.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return 'Logged out successfully'


@fastapi_app.get("/get_subscriptions")
async def get_all_subscriptions():
    subscriptions = await orchestrator.get_all_subscriptions()
    return {"subscriptions": subscriptions}

@fastapi_app.post("/add_subscription")
async def add_subscription(request: SubscriptionRequest):
    result = await orchestrator.add_subscription(request.email, request.subscription_type)
    return result

@fastapi_app.put("/extend_subscription/{email}")
async def extend_subscription(email: str, amount: int):
    print(f"Received email: {email}, amount: {amount}")
    result = await orchestrator.extend_subscription(email, amount)
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


@fastapi_app.get("/get_subscription/{user_id}")
async def get_subscription(user_id: int):
    result = await orchestrator.get_subscription(user_id=user_id)
    return result

@fastapi_app.get("/user_details/{user_id}")
async def get_user_details(user_id: int, request: Request):
    user = request.session.get('user')
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated, please login first to access this.')
    result = await orchestrator.get_user(user_id=user_id)
    return result

@fastapi_app.post("/add_user")
async def add_user(user: User):
    result = await orchestrator.add_user(
        username=user.username, email=user.email, password=user.password
    )   
    return result

@fastapi_app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, request: Request):
    user = request.session.get('user')
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated, please login first to access this.')
    result = await orchestrator.delete_user(user_id=user_id)
    return result

@fastapi_app.patch("/update_password/{user_id}")
async def update_password(user_id: int, passwords: UpdatePassword, request: Request):
    user = request.session.get('user')
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated, please login first to access this.')
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
