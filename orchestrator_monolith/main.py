import uvicorn
from fastapi import FastAPI
from orchestrator_monolith.src.orchestrator.router import fastapi_app
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret", max_age=100)
app.include_router(fastapi_app)

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8000)
