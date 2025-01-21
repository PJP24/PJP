import uvicorn
from fastapi import FastAPI
from src.orchestrator.router import fastapi_app

app = FastAPI()

app.include_router(fastapi_app)

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8000)
