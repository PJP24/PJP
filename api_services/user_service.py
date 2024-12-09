import grpc
from grpc_gen.generated.user_pb2 import UserRequest
from grpc_gen.generated.user_pb2_grpc import UserServiceStub

class UserServiceAPI:
    def __init__(self, host):
        self.host = host

    async def fetch_user_data(self, user_id: str):
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = UserServiceStub(channel)
            request = UserRequest(user_id=user_id)
            response = await stub.GetUserDetails(request)
            if response.user_id:
                return {'user_id': f'{response.user_id}', 'name': response.name, 'email': response.email}
            return None
