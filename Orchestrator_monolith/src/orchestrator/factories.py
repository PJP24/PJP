from src.services.users_service.user_api import UserServiceAPI
from src.services.subscriptions_service.subscription_api import SubscriptionServiceAPI

def user_service_api() -> UserServiceAPI:
    return UserServiceAPI(host="user_service:50051")

def subscription_service_api() -> SubscriptionServiceAPI:
    return SubscriptionServiceAPI(host="subscription_service:50052")