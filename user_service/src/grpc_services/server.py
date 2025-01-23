from user_service.src.grpc_services.generated.user_pb2 import (
    Response,
    User,
    Id,
    UserDetails,
    UpdatePassword,
    CreateUserResponse,
    GetUserIdRequest,
    GetUserIdResponse
)
from user_service.src.grpc_services.generated.user_pb2_grpc import UserManagementServicer
from grpc import RpcError
from sqlalchemy.exc import IntegrityError
from user_service.src.grpc_services.user_crud import UserCrud
from user_service.src.utils.validators import is_valid_email, is_valid_password, is_valid_username


class UserManagement(UserManagementServicer):
    def __init__(self, user_crud: UserCrud):
        self.user_crud = user_crud

    async def create(self, request: User, context) -> Response:
        print("Got request to create user: \n" + str(request))
        if not is_valid_username(request.username):
            return CreateUserResponse(
                status="error",
                message="Username must be at least 5 characters long",
                username=None,
                email=None,
            )
        if not is_valid_email(request.email):
            return CreateUserResponse(
                status="error",
                message="Invalid email",
                username=None,
                email=None,
            )
        if not is_valid_password(request.password):
            return CreateUserResponse(
                status="error",
                message="Password is not strong enough.",
                username=None,
                email=None,
            )
        try:
            result = await self.user_crud.create(request)
            if result == "success":
                return CreateUserResponse(
                    status="success",
                    message="User created successfully",
                    username=request.username,
                    email=request.email,
                )
        except IntegrityError:
            return CreateUserResponse(
                status="error",
                message="Account already exists with this username/email",
                username=None,
                email=None,
            )
        except RpcError as e:
            print(f"gRPC error: {e}")
            return CreateUserResponse(
                status="error",
                message="An error occured while processing your request.",
                username=None,
                email=None,
            )

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
            return Response(status="error", message="User not found.")
        else:
            if request.old_password == user.password:
                if not is_valid_password(request.new_password):
                    return Response(
                        status="error",
                        message="New password is not strong enoug.",
                    )
                else:
                    await self.user_crud.update_password(user.id, request.new_password)
                    return Response(
                        status="success",
                        message=f"Password successfully updated for user with ID {request.user_id.id}",
                    )
            return Response(status="error", message="Passwords do not match.")

    async def delete(self, request: Id, context) -> Response:
        print(f"Got request to delete user with id {request.id}")
        user = await self.user_crud.read(request.id)
        if user is None:
            return Response(status="error", message="User not found.")
        await self.user_crud.delete(user.id)
        return Response(
            status="success",
            message=f"User with Id {request.id} was deleted successfully.",
        )


    async def get_user_id(self, request: GetUserIdRequest, context) -> Id:
        user = await self.user_crud.get_user_by_email(request.email)
        print(user)
        if user is None:
            return GetUserIdResponse(status='error')
        return GetUserIdResponse(status=str(user.id))