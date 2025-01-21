import asyncio
import grpc

from src.grpc_services.generated.user_pb2 import Id, User, UpdatePassword, DeleteUser
from src.grpc_services.generated.user_pb2_grpc import UserManagementStub
from src.utils.validators import is_valid_username, is_valid_email, is_valid_password


class Client:
    def __init__(self, address: str) -> None:
        self.channel = grpc.aio.insecure_channel(address)
        self.stub = UserManagementStub(self.channel)

    async def read(self):
        try:
            response = await self.stub.read(Id(id=int(input("Please enter Id: "))))
            print(f"Username: {response.username}\nEmail: {response.email}")
        except ValueError:
            print("Invalid ID. Please enter correct ID.")

    async def create(self):
        username = input("Username: ")
        if not is_valid_username(username):
            print("Username must be at least 5 characters long")
            return
        email = input("Email: ")
        if not is_valid_email(email):
            print("Invalid email")
            return
        password = input("Password: ")
        if not is_valid_password(password):
            print("Password is not strong enough.")
            return
        confirm_password = input("Confirm password: ")
        if not password == confirm_password:
            print("Passwords do not match.")
            return
        response = await self.stub.create(
            User(
                username=username,
                email=email,
                password=password,
            )
        )
        print(response.message)

    async def update_password(self):
        user_id = int(input("User ID: "))
        old_password = input("Old password: ")
        new_password = input("New password: ")
        response = await self.stub.update_password(
            UpdatePassword(
                user_id=Id(id=user_id),
                old_password=old_password,
                new_password=new_password,
            )
        )
        print(response.message)

    async def delete(self):
        user_id = int(input("User ID: "))
        confirmation = input("Confirm Y/N: ").strip().lower()
        if confirmation == "y":
            confirmation = True
        else:
            confirmation = False
        response = await self.stub.delete(
            DeleteUser(user_id=Id(id=user_id), confirm_delete=confirmation)
        )
        print(response.message)

    async def close(self):
        await self.channel.close()


async def main():
    client = Client("localhost:50051")
    while True:
        action = input("What would you like to do?: ").strip().lower()
        if action == "create":
            await client.create()
        elif action == "read":
            await client.read()
        elif action == "update password":
            await client.update_password()
        elif action == "delete":
            await client.delete()
        else:
            print("Exiting.")
            break
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
