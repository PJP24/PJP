import asyncio
from src.grpc.config import DATABASE_URL as db_url
from src.db.database import init_db
from src.grpc.start_grpc_server import start_grpc_server

async def main():
    db = await init_db(db_url)
    await start_grpc_server(db)

if __name__ == '__main__':
    asyncio.run(main())
