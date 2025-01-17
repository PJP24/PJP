from fastapi import FastAPI
from pydantic import BaseModel
from src.orchestrator.orchestrator import Orchestrator

app = FastAPI()

orchestrator = Orchestrator()

class SubscriptionRequest(BaseModel):
    email: str
    subscription_type: str

@app.get("/subscriptions")
async def get_all_subscriptions():
    print(222)
    subscriptions = await orchestrator.get_all_subscriptions()    
    print(f"Subscriptions: {subscriptions}")
    return {"subscriptions": subscriptions}

@app.post("/subscriptions")
async def add_subscription(request: SubscriptionRequest):
    result = await orchestrator.add_subscription(request.email, request.subscription_type)
    return result

@app.put("/subscriptions")
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
