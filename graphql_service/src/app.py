import strawberry.asgi
from graphql_service.src.schema import Query, Mutation
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = strawberry.asgi.GraphQL(schema)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_route("/graphql", graphql_app)
