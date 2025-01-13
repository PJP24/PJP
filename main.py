import asyncio
import uvicorn
from orchestrator.fastapi_service import app
from user_service.user_service_server import main_user as serve_user
from subscription_service.subscription_service_server import main_subscription as serve_subscription


async def start_api_service():
    config = uvicorn.Config(app, host="0.0.0.0", port=5001, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def start_graphql():
    config = uvicorn.Config(app, host="0.0.0.0", port=8001, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        serve_user(),
        serve_subscription(),
        start_api_service(),
        start_graphql(),
    )

if __name__ == '__main__':
    asyncio.run(main())
