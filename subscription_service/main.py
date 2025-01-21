import asyncio
from src.grpc_services.config import DATABASE_URL as db_url
from src.grpc_services.start_grpc_server import start_grpc_server
from src.db.database import Database

async def main():
    db = Database(database_url=db_url)
    await start_grpc_server(db)

if __name__ == '__main__':
    asyncio.run(main())
