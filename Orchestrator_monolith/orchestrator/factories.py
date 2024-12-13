from api_services.user_service import UserServiceAPI
from api_services.subscription_service import SubscriptionServiceAPI

def get_user_service_api() -> UserServiceAPI:
    return UserServiceAPI(host="user_service:50051")  # Use service name here

def get_subscription_service_api() -> SubscriptionServiceAPI:
    return SubscriptionServiceAPI(host="subscription_service:50052")  # Use service name here
