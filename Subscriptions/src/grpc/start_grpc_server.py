from src.db.database import Database
import grpc
from src.grpc.generated.subscription_pb2_grpc import add_SubscriptionServiceServicer_to_server

from src.grpc.server import SubscriptionService


async def start_grpc_server(db: Database) -> None:
    server = grpc.aio.server()
    add_SubscriptionServiceServicer_to_server(SubscriptionService(database=db), server)

    server.add_insecure_port("[::]:50052")
    print("Starting server...")
    await server.start()
    await server.wait_for_termination()
