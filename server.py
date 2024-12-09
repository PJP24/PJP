import grpc
from grpc_gen.generated import user_pb2, user_pb2_grpc
from orchestrator.orchestrator import Orchestrator
import asyncio

USER_DB = {
    "1": {"user_id": "1", "name": "Alice Johnson", "email": "alice.johnson@example.com"},
    "2": {"user_id": "2", "name": "Carlos Martinez", "email": "carlos.martinez@example.com"},
    "3": {"user_id": "3", "name": "Emma Green", "email": "emma.green@example.com"},
    "4": {"user_id": "4", "name": "David Lee", "email": "david.lee@example.com"},
    "5": {"user_id": "5", "name": "Sophia Harris", "email": "sophia.harris@example.com"},
    "6": {"user_id": "6", "name": "Mohamed Ali", "email": "mohamed.ali@example.com"}
}


class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.orchestrator = Orchestrator()

    async def GetUserDetails(self, request, context):
        user_id = request.user_id
        user_data = USER_DB.get(user_id)

        if user_data:
            return user_pb2.UserResponse(
                user_id=user_data["user_id"],
                name=user_data["name"],
                email=user_data["email"]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_pb2.UserResponse()

# Start the gRPC server
async def grpc_server():
    server = grpc.aio.server()
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    print('gRPC Server is listening on port 50051')
    await server.start()
    await server.wait_for_termination()

def serve():
    asyncio.run(grpc_server())

if __name__ == "__main__":
    serve()
