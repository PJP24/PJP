import asyncio
import grpc
from src.orchestrator.generated import subscription_pb2, subscription_pb2_grpc
from src.database.subscription_repositories import SubscriptionRepository

class SubscriptionService(subscription_pb2_grpc.SubscriptionServiceServicer):
    def __init__(self, subscription_repository: SubscriptionRepository):
        self.subscription_repository = subscription_repository

    def _get_subscription_response(self, subscription_data: dict, context) -> subscription_pb2.SubscriptionResponse:
        if 'error' not in subscription_data:
            return subscription_pb2.SubscriptionResponse(
                user_id=subscription_data["user_id"],
                subscription_type=subscription_data["subscription_type"],
                period=subscription_data["period"]
            )
        context.set_code(grpc.StatusCode.NOT_FOUND if 'user_id' in subscription_data else grpc.StatusCode.INTERNAL)
        return subscription_pb2.SubscriptionResponse()

    async def GetSubscriptionDetails(self, request: subscription_pb2.SubscriptionRequest,
                                     context: grpc.ServicerContext) -> subscription_pb2.SubscriptionResponse:
        subscription_data = self.subscription_repository.get_subscription_by_user_id(request.user_id)
        return self._get_subscription_response(subscription_data, context)

    async def AddSubscription(self, request, context):
        subscription_data = self.subscription_repository.add_subscription(request.user_id, request.subscription_type, request.period)
        return self._get_subscription_response(subscription_data, context)


async def start_subscription_server():
    subscription_server = grpc.aio.server()
    subscription_service = SubscriptionService(SubscriptionRepository())
    subscription_pb2_grpc.add_SubscriptionServiceServicer_to_server(subscription_service, subscription_server)
    subscription_server.add_insecure_port("[::]:50052")
    await subscription_server.start()
    print("Server subscription started on port 50052")
    await subscription_server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(start_subscription_server())
