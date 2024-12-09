import asyncio
from grpc.aio import Server
from services.services import start_user_service, start_subscription_service

async def main() -> None:
    user_server: Server = await start_user_service()
    subscription_server: Server = await start_subscription_service()

    await asyncio.gather(
        user_server.wait_for_termination(),
        subscription_server.wait_for_termination()
    )

if __name__ == "__main__":
    asyncio.run(main())
