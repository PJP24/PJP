import strawberry.asgi
from schema import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = strawberry.asgi.GraphQL(schema)
