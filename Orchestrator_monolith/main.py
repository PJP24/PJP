import uvicorn
from fastapi import FastAPI
from src.orchestrator.router import users_router, subscriptions_router

app = FastAPI()

app.include_router(users_router)
app.include_router(subscriptions_router)


if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8000)
