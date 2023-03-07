from strawberry.asgi import GraphQL
from typing import Any, Optional

class MyGrapQL(GraphQL):
    def __init__( self, schema ):
        self._roles = None
        super().__init__(schema) 

    async def get_context(self, request, response = None) -> Optional[Any]:
        return {"request": request, "response": response, "roles": self.roles}
    
    @property
    def roles(self):
        return self._roles
    
    @roles.setter
    def roles(self, value):
        self._roles = value 