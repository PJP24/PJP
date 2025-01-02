import grpc
from src.services.generated import user_pb2, user_pb2_grpc

# from src.services.generated import user_pb2, user_pb2_grpc

from typing import Dict
# from src.database.utils.user_id_generator import UserIdGenerator

class UserServiceAPI:
    def __init__(self, host: str):
        self.host = host
        # self.next_id = UserIdGenerator(table_name="users")

    async def _make_grpc_call(self, method: str, request) -> Dict[str, str]:
        async with grpc.aio.insecure_channel(self.host) as channel: 
            stub = user_pb2_grpc.UserManagementStub(channel)
            try:
                response = await getattr(stub, method)(request)
                return response
                # return {
                #     # "user_id": response.user_id,
                #     "username": response.username,
                #     "email": response.email,
                # }
            except grpc.RpcError as e:
                return {"error": f"gRPC error: {e.code()} - {e.details()}"}
            except Exception as e:
                print (e)
                return {"error": str(e)}

    async def fetch_user_data(self, user_id: str) -> Dict[str, str]:
        request = user_pb2.Id(id=int(user_id))
        response = await self._make_grpc_call('read', request)
        if response.username: 
            return {
                    # "user_id": response.user_id,
                    "username": response.username,
                    "email": response.email,
                }
    async def add_user(self, username: str, email: str, password: str) -> Dict[str, str]:
        request = user_pb2.User(username=username, email=email, password=password)
        return await self._make_grpc_call('create', request)

#     async def update_user(self, user_id: str, name: str, email: str) -> Dict[str, str]:
#         request = user_pb2.UserUpdateRequest(user_id=user_id, name=name, email=email)
#         return await self._make_grpc_call('UpdateUser', request)

    async def delete_user(self, user_id: str, confirmation: bool) -> Dict[str, str]:
        request = user_pb2.DeleteUser(user_id=(user_pb2.Id(id=int(user_id))), confirm_delete=confirmation)
        return await self._make_grpc_call('delete', request)
