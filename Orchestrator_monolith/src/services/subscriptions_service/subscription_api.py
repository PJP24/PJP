import grpc
from src.services.generated import subscription_pb2, subscription_pb2_grpc
from typing import Dict
from src.database.utils.user_id_generator import UserIdGenerator

class SubscriptionServiceAPI:
    def __init__(self, host: str):
        self.host = host
        self.next_id = UserIdGenerator(table_name="subscriptions")

    async def _make_grpc_call(self, method: str, request) -> Dict[str, str]:
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            try:
                response = await getattr(stub, method)(request)
                return {
                    "user_id": response.user_id,
                    "subscription_type": response.subscription_type,
                    "period": response.period,
                }
            except grpc.RpcError as e:
                return {"error": f"gRPC error: {e.code()} - {e.details()}"}
            except Exception as e:
                return {"error": str(e)}


    async def fetch_subscription_data(self, user_id: str) -> Dict[str, str]:
        request = subscription_pb2.SubscriptionRequest(user_id=user_id)
        return await self._make_grpc_call('GetSubscriptionDetails', request)

    async def add_subscription(self, subscription_type: str, period: str) -> Dict[str, str]:
        next_user_id = self.next_id.get_next_user_id()
        if isinstance(next_user_id, dict) and "error" in next_user_id:
            return next_user_id
        user_id = next_user_id
        request = subscription_pb2.SubscriptionRequest(user_id=user_id, subscription_type=subscription_type,
                                                       period=period)
        return await self._make_grpc_call('AddSubscription', request)
