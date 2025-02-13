import strawberry.asgi
from graphql_service.src.schema import Query, Mutation
from starlette.middleware.cors import CORSMiddleware
from starlette.applications import Starlette


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = strawberry.asgi.GraphQL(schema)


app = Starlette()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],  
    allow_headers=["*"],  
    allow_credentials=True
)

app.mount("/", graphql_app)


