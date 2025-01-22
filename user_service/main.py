import asyncio
import grpc
from user_service.src.grpc_services import config
from user_service.src.grpc_services.server import UserManagement
from user_service.src.grpc_services.user_crud import UserCrud
from user_service.src.db.database import Database
from user_service.src.grpc_services.generated import user_pb2_grpc


DB_URL = config.DB_URL


async def serve(db: Database):
    server = grpc.aio.server()
    user_crud = UserCrud(db)
    user_pb2_grpc.add_UserManagementServicer_to_server(
        UserManagement(user_crud=user_crud), server
    )
    server.add_insecure_port("0.0.0.0:50051")
    await server.start()
    print("Starting server on :50051")
    await server.wait_for_termination()


async def main():
    db = Database(database_url=DB_URL)
    await serve(db=db)


if __name__ == "__main__":
    asyncio.run(main())
