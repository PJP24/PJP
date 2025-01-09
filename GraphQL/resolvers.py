from typing import List
import requests

def get_all_subscriptions_resolver():
    from schema import Subscription
    response = requests.get("http://fastapi_service:8000/subscriptions")
    raw_subscriptions = response.json().get("subscriptions", [])
    return [Subscription(**sub) for sub in raw_subscriptions]

def add_subscription_resolver(email: str, subscription_type: str) -> str:
    response = requests.post(
        "http://fastapi_service:8000/subscriptions",
        json={"email": email, "subscription_type": subscription_type},
    )
    return response.json().get("message", "Unknown result")

def change_subscription_resolver(email: str, subscription_type: str) -> str:
    response = requests.put(
        "http://fastapi_service:8000/subscriptions",
        json={"email": email, "subscription_type": subscription_type},
    )
    return response.json().get("message", "Unknown result")

def delete_subscription_resolver(email: str) -> str:
    response = requests.delete(f"http://fastapi_service:8000/subscriptions/{email}")
    return response.json().get("message", "Unknown result")

def activate_subscription_resolver(email: str) -> str:
    response = requests.post(f"http://fastapi_service:8000/subscriptions/{email}/activate")
    return response.json().get("message", "Unknown result")

def deactivate_subscription_resolver(email: str) -> str:
    response = requests.post(f"http://fastapi_service:8000/subscriptions/{email}/deactivate")
    return response.json().get("message", "Unknown result")

def opt_out_policy_resolver() -> str:
    response = requests.get("http://fastapi_service:8000/opt-out-policy")
    return response.json().get("policy", "No policy available")
