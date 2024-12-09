import grpc
from grpc_gen.generated.user_pb2 import UserRequest
from grpc_gen.generated.user_pb2_grpc import UserServiceStub
from typing import Dict, Optional

class UserServiceAPI:
    def __init__(self, host: str):
        self.host: str = host

    async def fetch_user_data(self, user_id: str) -> Dict[str, Optional[str]]:
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = UserServiceStub(channel)
                request = UserRequest(user_id=user_id)
                response = await stub.GetUserDetails(request)
                if response.user_id:
                    return {'user_id': response.user_id, 'name': response.name, 'email': response.email}
                return {"error": "User not found"}
        except grpc.aio.AioRpcError as e:
            return {"error": f"An error occurred while fetching user data: No such User ID"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
