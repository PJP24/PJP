import grpc
from src.orchestrator.generated import subscription_pb2, subscription_pb2_grpc
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
                return response
            except grpc.RpcError as e:
                return {"error": f"gRPC error: {e.code()} - {e.details()}"}
            except Exception as e:
                return {"error": str(e)}
            

    async def fetch_all_subscriptions(self):
        from src.graphql.schema import Subscription

        request = subscription_pb2.GetSubscriptionsRequest()
        response = await self._make_grpc_call('GetSubscriptions', request)

        subscriptions = [Subscription(username=sub.email, subscription_type=sub.subscription_type) for sub in response.subscriptions]

        return subscriptions
