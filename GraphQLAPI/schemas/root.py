
import strawberry
from strawberry.schema.config import StrawberryConfig
from strawberry.extensions import QueryDepthLimiter, AddValidationRules
from graphql.validation import NoSchemaIntrospectionCustomRule
from strawberry.tools import merge_types
from os import environ

from GraphQLAPI.schemas.person import PersonsQuery
from GraphQLAPI.schemas.NYC_taxis import TaxisQuery

# Combine all root special Query types.
BaseQuery = merge_types("BaseQuery", (PersonsQuery, TaxisQuery) )

# Add base schema extensions.
extensions = [
  QueryDepthLimiter(max_depth=3),
  AddValidationRules([NoSchemaIntrospectionCustomRule])
]

# Add .
debug = environ.get('DEBUG').lower()
if debug == 'true':
  extensions = [
    QueryDepthLimiter(max_depth=3),
  ]


schema = strawberry.Schema(
                      query=BaseQuery, 
                      config=StrawberryConfig(auto_camel_case=False),
                      extensions=extensions,
                    )