import strawberry
from GraphQLAPI.utils.scalar import Base64
from GraphQLAPI.utils.permissions import IsAuthorized
from GraphQLAPI.utils.directives import Auth

@strawberry.type(directives=[Auth(role='ADMIN')])
class CalculatedQuery:

    @strawberry.field(permission_classes=[IsAuthorized])
    def base64(self, nput:str)-> Base64:
      return Base64(str.encode(nput))
    