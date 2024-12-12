import asyncio
from grpc.aio import Server
from services.services import start_subscription_service

async def main_subscription_service() -> None:
    subscription_server: Server = await start_subscription_service()
    print("server user started")
    await subscription_server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(main_subscription_service())
