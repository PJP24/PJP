import grpc
from src.services.generated import user_pb2, user_pb2_grpc
from typing import Dict
from src.database.utils.user_id_generator import UserIdGenerator

class UserServiceAPI:
    def __init__(self, host: str):
        self.host = host
        self.next_id = UserIdGenerator(table_name="users")

    async def _make_grpc_call(self, method: str, request) -> Dict[str, str]:
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            try:
                response = await getattr(stub, method)(request)
                return {
                    "user_id": response.user_id,
                    "name": response.name,
                    "email": response.email,
                }
            except grpc.RpcError as e:
                return {"error": f"gRPC error: {e.code()} - {e.details()}"}
            except Exception as e:
                return {"error": str(e)}

    async def fetch_user_data(self, user_id: str) -> Dict[str, str]:
        request = user_pb2.UserRequest(user_id=user_id)
        return await self._make_grpc_call('GetUserDetails', request)

    async def add_user(self, name: str, email: str) -> Dict[str, str]:
        next_user_id = self.next_id.get_next_user_id()

        if isinstance(next_user_id, dict) and "error" in next_user_id:
            return next_user_id

        user_id = next_user_id
        request = user_pb2.UserRequest(user_id=user_id, name=name, email=email)

        return await self._make_grpc_call('AddUser', request)

    async def update_user(self, user_id: str, name: str, email: str) -> Dict[str, str]:
        request = user_pb2.UserUpdateRequest(user_id=user_id, name=name, email=email)
        return await self._make_grpc_call('UpdateUser', request)

    async def delete_user(self, user_id: str) -> Dict[str, str]:
        request = user_pb2.UserRequest(user_id=user_id)
        return await self._make_grpc_call('DeleteUser', request)
