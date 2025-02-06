from temporalio import activity
import grpc


from orchestrator_monolith.src.generated.user_pb2 import UserId
from orchestrator_monolith.src.generated.user_pb2_grpc import UserManagementStub



class DSLActivities:
    @activity.defn
    async def delete_user_activity(self, user_id: int):
        try:
            request = UserId(id=user_id)
            async with grpc.aio.insecure_channel("user_service_container:50051") as channel:
                stub = UserManagementStub(channel)
                response = await stub.DeleteUser(request)
                return {"status": response.status, "message": response.message}
        except Exception as e:
            return {"error": f"Error deleting user: {str(e)}"}
