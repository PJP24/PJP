from api_services.user_service import UserServiceAPI

def get_user_service_api():
    return UserServiceAPI(host="localhost:50051")
