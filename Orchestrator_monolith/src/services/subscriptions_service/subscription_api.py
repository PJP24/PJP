import grpc
from src.orchestrator.generated import subscription_pb2, subscription_pb2_grpc

class SubscriptionServiceAPI:
    def __init__(self, host: str):
        self.host = host

    async def fetch_all_subscriptions(self):
        from src.graphql.schema import Subscription

        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = subscription_pb2_grpc.SubscriptionServiceStub(channel)
            request = subscription_pb2.GetSubscriptionsRequest()
            response = await stub.GetSubscriptions(request)

        subscriptions = [Subscription(username=sub.email, subscription_type=sub.subscription_type) for sub in response.subscriptions]

        return subscriptions
