from user_service.src.grpc_services.generated.user_pb2 import (
    Response,
    CreateUserRequest,
    UserId,
    UserDetails,
    UpdatePassword,
    CreateUserResponse,
    GetUserIdRequest,
    GetUserIdResponse,
    GetEmailsRequest,
    GetEmailsResponse
)
from user_service.src.grpc_services.generated.user_pb2_grpc import UserManagementServicer
from grpc import RpcError
from sqlalchemy.exc import IntegrityError
from user_service.src.grpc_services.user_crud import UserCrud
from user_service.src.utils.validators import is_valid_email, is_valid_password, is_valid_username


class UserManagement(UserManagementServicer):
    def __init__(self, user_crud: UserCrud):
        self.user_crud = user_crud

    async def CreateUser(self, request: CreateUserRequest, context) -> CreateUserResponse:
        print("Got request to create user: \n" + str(request))
        if not is_valid_username(request.username):
            return CreateUserResponse(
                status="error",
                message="Username must be at least 5 characters long",
                username=None,
                email=None,
                id=None,
            )
        if not is_valid_email(request.email):
            return CreateUserResponse(
                status="error",
                message="Invalid email",
                username=None,
                email=None,
                id=None,
            )
        if not is_valid_password(request.password):
            return CreateUserResponse(
                status="error",
                message="Password is not strong enough.",
                username=None,
                email=None,
                id=None,
            )
        try:
            result = await self.user_crud.create_user(request)
            if result:
                return CreateUserResponse(
                    status="success",
                    message="User created successfully",
                    username=request.username,
                    email=request.email,
                    id = result,
                )
        except IntegrityError:
            return CreateUserResponse(
                status="error",
                message="Account already exists with this username/email",
                username=None,
                email=None,
                id = None,
            )
        except RpcError as e:
            print(f"gRPC error: {e}")
            return CreateUserResponse(
                status="error",
                message="An error occured while processing your request.",
                username=None,
                email=None,
                id = None,
            )

    async def GetUserDetails(self, request: UserId, context) -> UserDetails:
        print("Got request to get user with: \n" + str(request))
        user = await self.user_crud.get_user(request.id)
        if user:
            username = user.username
            email = user.email
            return UserDetails(username=username, email=email)
        return UserDetails(username="", email="")

    async def UpdateUserPassword(self, request: UpdatePassword, context) -> Response:
        print(f"Got request to update password of user : {request.user_id.id}")
        user = await self.user_crud.get_user(request.user_id.id)
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

    async def DeleteUser(self, request: UserId, context) -> Response:
        print(f"Got request to delete user with id {request.id}")
        user = await self.user_crud.get_user(request.id)
        if user is None:
            return Response(status="error", message="User not found.")
        await self.user_crud.delete_user(user.id)
        return Response(
            status="success",
            message=f"User with Id {request.id} was deleted successfully.",
        )


    async def GetUserId(self, request: GetUserIdRequest, context) -> GetUserIdResponse:
        user = await self.user_crud.get_user_by_email(request.email)
        print(user)
        if user is None:
            return GetUserIdResponse(status='error')
        return GetUserIdResponse(status=str(user.id))
    

    async def GetUsersEmails(self, request: GetEmailsRequest, context) -> GetEmailsResponse:
        users_emails = await self.user_crud.get_user_emails(request.id)
        return GetEmailsResponse(email=users_emails)