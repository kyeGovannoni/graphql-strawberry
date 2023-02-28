import strawberry
from GraphQLAPI.utils.scalar import Base64


@strawberry.type
class CalculatedQuery:

    @strawberry.field
    def base64(self, nput:str)-> Base64:
      return Base64(str.encode(nput))