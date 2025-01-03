import asyncio
import grpc
from src.orchestrator.generated import user_pb2, user_pb2_grpc
from src.database.user_repositories import UserRepository

class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _get_user_response(self, user_data: dict, context) -> user_pb2.UserResponse:
        if 'error' not in user_data:
            return user_pb2.UserResponse(
                user_id=user_data["user_id"],
                name=user_data["name"],
                email=user_data["email"]
            )
        context.set_code(grpc.StatusCode.NOT_FOUND if 'user_id' in user_data else grpc.StatusCode.INTERNAL)
        return user_pb2.UserResponse()

    async def GetUserDetails(self, request: user_pb2.UserRequest, context: grpc.ServicerContext) -> user_pb2.UserResponse:
        user_data = self.user_repository.get_user_by_user_id(request.user_id)
        return self._get_user_response(user_data, context)

    async def AddUser(self, request, context):
        user_data = self.user_repository.add_user(request.user_id, request.name, request.email)
        return self._get_user_response(user_data, context)

    async def UpdateUser(self, request: user_pb2.UserUpdateRequest, context) -> user_pb2.UserResponse:
        user_data = self.user_repository.update_user(request.user_id, request.name, request.email)
        return self._get_user_response(user_data, context)

    async def DeleteUser(self, request: user_pb2.UserRequest, context) -> user_pb2.UserResponse:
        user_data = self.user_repository.delete_user(request.user_id)
        if 'error' not in user_data:
            context.set_code(grpc.StatusCode.OK)
            return user_pb2.UserResponse(message=user_data['message'])
        return self._get_user_response(user_data, context)

async def start_user_server():
    user_server = grpc.aio.server()
    user_service = UserService(UserRepository())
    user_pb2_grpc.add_UserServiceServicer_to_server(user_service, user_server)
    user_server.add_insecure_port("[::]:50051")
    await user_server.start()
    print("Server user started on port 50051")
    await user_server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(start_user_server())
