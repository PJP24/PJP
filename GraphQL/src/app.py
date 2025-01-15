import strawberry.asgi
from src.schema import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = strawberry.asgi.GraphQL(schema)
