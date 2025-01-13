import grpc
import asyncio
from grpc import RpcError
from sqlalchemy.exc import IntegrityError
from user_service.utils.config import DB_URL
from user_service.db.database import Database
from user_service.grpc_services.generated import user_pb2_grpc
from user_service.grpc_services.generated.user_pb2_grpc import UserManagementServicer
from user_service.grpc_services.user_db_operations import UserManager
from user_service.utils.validators import is_valid_email, is_valid_password, is_valid_username
from user_service.grpc_services.generated.user_pb2 import (
    Response,
    User,
    Id,
    UserDetails,
    UpdatePassword,
    CreateUserResponse,
)



class UserManagement(UserManagementServicer):
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    async def create(self, request: User, context) -> Response:
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
            result = await self.user_manager.create(request)
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
            return CreateUserResponse(
                status="error",
                message="An error occured while processing your request.",
                username=None,
                email=None,
            )

    async def read(self, request: Id, context) -> UserDetails:
        user = await self.user_manager.read(request.id)
        if user:
            username = user.username
            email = user.email
            return UserDetails(username=username, email=email)
        return UserDetails(username="", email="")

    async def update_password(self, request: UpdatePassword, context) -> Response:
        user = await self.user_manager.read(request.user_id.id)
        if user is None:
            return Response(status="error", message="User not found.")
        else:
            if request.old_password == user.password:
                if not is_valid_password(request.new_password):
                    return Response(
                        status="error",
                        message="New password is not strong enough.",
                    )
                else:
                    await self.user_manager.update_password(user.id, request.new_password)
                    return Response(
                        status="success",
                        message=f"Password successfully updated for user with ID {request.user_id.id}",
                    )
            return Response(status="error", message="Passwords do not match.")

    async def delete(self, request: Id, context) -> Response:
        user = await self.user_manager.read(request.id)
        if user is None:
            return Response(status="error", message="User not found.")
        await self.user_manager.delete(user.id)
        return Response(
            status="success",
            message=f"User with Id {request.id} was deleted successfully.",
        )


async def serve_user(db: Database):
    server = grpc.aio.server()
    user_manager = UserManager(db)
    user_pb2_grpc.add_UserManagementServicer_to_server(UserManagement(user_manager=user_manager), server)
    server.add_insecure_port('[::]:50051')

    await server.start()
    print("Starting server on :50051")
    await server.wait_for_termination()

async def main_user():
    db = Database(database_url=DB_URL)
    await serve_user(db=db)

if __name__ == "__main__":
    asyncio.run(main_user())
