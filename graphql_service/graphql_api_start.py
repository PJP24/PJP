import logging
import asyncio
import uvicorn
from graphql_app import graphql_app as app

async def start_graphql():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting graphql service on port 8001...")
    config = uvicorn.Config(app, host="0.0.0.0", port=8001, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(start_graphql())
