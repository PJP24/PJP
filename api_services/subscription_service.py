import grpc
from grpc_gen.generated.subscription_pb2 import SubscriptionRequest
from grpc_gen.generated.subscription_pb2_grpc import SubscriptionServiceStub
from typing import Dict, Optional

class SubscriptionServiceAPI:
    def __init__(self, host: str):
        self.host: str = host

    async def fetch_subscription_data(self, user_id: str) -> Dict[str, Optional[str]]:
        try:
            async with grpc.aio.insecure_channel(self.host) as channel:
                stub = SubscriptionServiceStub(channel)
                request = SubscriptionRequest(user_id=user_id)
                response = await stub.GetSubscriptionDetails(request)
                if response.user_id:
                    return {'subscription_type': response.subscription_type, 'period': response.period}
                return {"error": "Subscription not found"}
        except grpc.aio.AioRpcError as e:
            return {"error": f"An error occurred while fetching subscription data: {e.details()}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
