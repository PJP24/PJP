import logging
import asyncio
import uvicorn
from orchestrator.fastapi_service import app


async def start_api_service():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting orchestrator service on port 5001...")
    config = uvicorn.Config(app, host="0.0.0.0", port=5001, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(start_api_service())