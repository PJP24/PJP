import strawberry
from graphql_service.src.schema import Query, Mutation
from strawberry.asgi import GraphQL
from starlette.requests import Request
from typing import Optional
from starlette.responses import Response

schema = strawberry.Schema(query=Query, mutation=Mutation)


class MyGraphQL(GraphQL):
    async def get_context(
        self, request: Request, response: Optional[Response] = None
    ):
        authentication_header = request.headers.get("Authentication")
        token = None
        if authentication_header:
            if authentication_header.startswith("Bearer "):
                token = authentication_header[len("Bearer "):]

        return {"token": token}


app = MyGraphQL(schema)