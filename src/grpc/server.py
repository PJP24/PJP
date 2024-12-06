from src.grpc.generated.user_pb2 import (
    Response,
    User,
    Id,
    UserDetails,
    UpdatePassword,
    DeleteUser,
)
from src.grpc.generated.user_pb2_grpc import UserManagementServicer
from grpc import RpcError
from src.grpc.user_crud import UserCrud


class UserManagement(UserManagementServicer):
    def __init__(self, user_crud: UserCrud):
        self.user_crud = user_crud

    async def create(self, request: User, context) -> Response:
        print("Got request to create user: \n" + str(request))
        try:
            result = await self.user_crud.create(request)
            if result == "success":
                return Response(message=f"Created user {request.username}")
            return Response(message=result)
        except RpcError as e:
            print(f"gRPC error: {e}")
            return Response(message="An error occured while processing your request.")

    async def read(self, request: Id, context) -> UserDetails:
        print("Got request to get user with: \n" + str(request))
        user = await self.user_crud.read(request.id)
        if user:
            username = user.username
            email = user.email
            return UserDetails(username=username, email=email)
        return UserDetails(username="", email="")

    async def update_password(self, request: UpdatePassword, context) -> Response:
        print(f"Got request to update password of user : {request.user_id.id}")
        user = await self.user_crud.read(request.user_id.id)
        if user is None:
            return Response(message="User not found.")
        else:
            if request.old_password == user.password:
                await self.user_crud.update_password(user.id, request.new_password)
                return Response(
                    message=f"Password successfully updated for user with ID {request.user_id.id}"
                )
            return Response(message="Passwords do not match.")

    async def delete(self, request: DeleteUser, context) -> Response:
        print(f"Got request to delete user with id {request.user_id.id}")
        user = await self.user_crud.read(request.user_id.id)
        conf = request.confirm_delete
        if user is None:
            return Response(message="User not found.")
        if conf:
            await self.user_crud.delete(user.id)
            return Response(
                message=f"User with Id {request.user_id.id} was deleted successfully."
            )
        return Response(
            message="Delete confirmation was not received and could not delete user."
        )
