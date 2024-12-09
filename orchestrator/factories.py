from api_services.user_service import UserServiceAPI
from api_services.subscription_service import SubscriptionServiceAPI

def get_user_service_api() -> UserServiceAPI:
    return UserServiceAPI(host="localhost:50051")

def get_subscription_service_api() -> SubscriptionServiceAPI:
    return SubscriptionServiceAPI(host="localhost:50052")
