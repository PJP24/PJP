import strawberry.asgi
from graphql_service.src.schema import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = strawberry.asgi.GraphQL(schema)



