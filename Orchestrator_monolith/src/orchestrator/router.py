from fastapi import FastAPI
from pydantic import BaseModel
from src.orchestrator.orchestrator import Orchestrator

app = FastAPI()

orchestrator = Orchestrator()

class SubscriptionRequest(BaseModel):
    email: str
    subscription_type: str

class ExtendSubscriptionRequest(BaseModel):
    email: str
    period: str  

@app.get("/subscriptions")
async def get_all_subscriptions():
    subscriptions = await orchestrator.get_all_subscriptions()    
    print(f"Subscriptions: {subscriptions}")
    return {"subscriptions": subscriptions}

@app.post("/subscriptions")
async def add_subscription(request: SubscriptionRequest):
    result = await orchestrator.add_subscription(request.email, request.subscription_type)
    return result

@app.put("/subscriptions")
async def extend_subscription(request: ExtendSubscriptionRequest):
    result = await orchestrator.extend_subscription(request.email, request.period)  
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
