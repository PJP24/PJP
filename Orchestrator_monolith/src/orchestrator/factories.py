from src.services.users_service.user_api import UserServiceAPI

def user_service_api() -> UserServiceAPI:
    return UserServiceAPI(host="user_service:50051")
