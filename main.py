import asyncio
import os
from dotenv import load_dotenv
from src.db.database import init_db
from src.grpc.start_grpc_server import start_grpc_server

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')

async def main():
    db = await init_db(DATABASE_URL)
    await start_grpc_server(db)

if __name__ == '__main__':
    asyncio.run(main())
