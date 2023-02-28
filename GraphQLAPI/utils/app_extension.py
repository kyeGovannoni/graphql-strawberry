from strawberry.asgi import GraphQL
from typing import Any, Optional

class MyGrapQL(GraphQL):
    def __init__( self, schema, credentials = None):
        self.credentials = credentials
        super().__init__(schema) 

    async def get_context(self, request, response = None) -> Optional[Any]:
        return {"request": request, "response": response, "credentials": self.credentials}