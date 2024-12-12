import asyncio
from grpc.aio import Server
from services.services import start_user_service

async def main_user_service() -> None:
    user_server: Server = await start_user_service()
    await user_server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(main_user_service())
