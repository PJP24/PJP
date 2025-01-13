import logging
from fastapi import FastAPI
from pydantic import BaseModel

from graphql_service.graphql_app import graphql_app
from orchestrator.orchestrator_service import OrchestratorService

app = FastAPI()

app.include_router(graphql_app, prefix='/graphql')

orchestrator = OrchestratorService()

class User(BaseModel):
    username: str
    email: str
    password: str


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str

class SubscriptionRequest(BaseModel):
    email: str
    subscription_type: str


@app.get("/user_details/{user_id}")
async def get_user_details(user_id: int):
    result = await orchestrator.get_user(user_id=user_id)
    return result


@app.post("/add_user")
async def add_user(user: User):
    result = await orchestrator.add_user(
        username=user.username, email=user.email, password=user.password
    )
    print(f"Result from orchestrator.add_user: {result}")
    return result


@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    result = await orchestrator.delete_user(user_id=user_id)
    return result


@app.patch("/update_password/{user_id}")
async def update_password(user_id: int, passwords: UpdatePassword):
    result = await orchestrator.update_user_password(
        user_id=user_id,
        old_password=passwords.old_password,
        new_password=passwords.new_password,
    )
    return result

@app.get("/get_subscriptions")
async def get_all_subscriptions():
    subscriptions = await orchestrator.get_all_subscriptions()

    return {"subscriptions": subscriptions}

@app.post("/add_subscriptions")
async def add_subscription(request: SubscriptionRequest):
    result = await orchestrator.add_subscription(request.email, request.subscription_type)
    print(result)
    return result


@app.put("/change_subscriptions")
async def change_subscription(request: SubscriptionRequest):
    result = await orchestrator.change_subscription(request.email, request.subscription_type)
    return result


@app.delete("/subscriptions/{email}")
async def delete_subscription(email: str):
    result = await orchestrator.delete_subscription(email)
    return result


@app.post("/subscriptions/{email}/activate")
async def activate_subscription(email: str):
    result = await orchestrator.activate_subscription(email)
    return result


@app.post("/subscriptions/{email}/deactivate")
async def deactivate_subscription(email: str):
    result = await orchestrator.deactivate_subscription(email)
    return result


@app.get("/opt-out-policy")
async def opt_out_policy():
    policy_text = await orchestrator.get_opt_out_policy()
    return {"policy": policy_text}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting orchestrator service on port 5001...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
