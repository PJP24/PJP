import asyncio
import grpc
from src.grpc.server import UserManagement
from src.grpc.user_crud import UserCrud


from src.db.database import Database
from src.grpc.generated import user_pb2_grpc
import config

DB_URL = config.DB_URL


async def serve(db: Database):
    server = grpc.aio.server()
    user_crud = UserCrud(db)
    user_pb2_grpc.add_UserManagementServicer_to_server(
        UserManagement(user_crud=user_crud), server
    )
    server.add_insecure_port("0.0.0.0:50051")
    print("Starting server on localhost:50051")
    await server.start()
    await server.wait_for_termination()
    # Block current thread until the server stops.


async def main():
    db = Database(database_url=DB_URL)
    await serve(db=db)


if __name__ == "__main__":
    asyncio.run(main())
