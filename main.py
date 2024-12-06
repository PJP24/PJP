import asyncio
import grpc
from src.grpc.server import UserManagement


from src.db.database import Database
from src.grpc.generated import user_pb2_grpc
import config

DB_URL = config.DB_URL

async def init_db():
    database = Database(database_url=DB_URL)
    await database.init_database()

    return database


async def serve(db: Database):
    server = grpc.aio.server()
    user_pb2_grpc.add_UserManagementServicer_to_server(
        UserManagement(database=db), server
    )
    server.add_insecure_port("0.0.0.0:50051")
    print("Starting server on localhost:50051")
    await server.start()
    await server.wait_for_termination()
    # Block current thread until the server stops.


async def main():
    db = await init_db()
    await serve(db=db)


if __name__ == "__main__":
    asyncio.run(main())
