import strawberry.asgi
from src.graphql.schema import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = strawberry.asgi.GraphQL(schema)
