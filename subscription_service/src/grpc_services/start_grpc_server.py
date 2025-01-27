import grpc
from subscription_service.src.db.database import Database
from subscription_service.src.grpc_services.generated.subscription_pb2_grpc import add_SubscriptionServiceServicer_to_server
from subscription_service.src.grpc_services.server import SubscriptionService


async def start_grpc_server(db: Database) -> None:
    server = grpc.aio.server()
    add_SubscriptionServiceServicer_to_server(SubscriptionService(database=db), server)

    server.add_insecure_port("0.0.0.0:50052")

    await server.start()
    print("Starting subscription server at 50052 ...")
    await server.wait_for_termination()
