
from strawberry import Schema
from strawberry.schema.config import StrawberryConfig
from strawberry.extensions import QueryDepthLimiter, AddValidationRules
from graphql.validation import NoSchemaIntrospectionCustomRule
from strawberry.tools import merge_types
from os import environ

# Graphql model query objects.
from GraphQLAPI.models._person import PersonsQuery
from GraphQLAPI.models._taxis import TaxisQuery
from GraphQLAPI.models._payment_types import PaymentTypeQuery
from GraphQLAPI.models._vendors import VendorQuery
from GraphQLAPI.models._calculated import CalculatedQuery

# Combine all root special Query types.
BaseQuery = merge_types("BaseQuery", (TaxisQuery, PaymentTypeQuery, VendorQuery, PersonsQuery, CalculatedQuery) )

# Add base schema extensions.
extensions = [
  QueryDepthLimiter(max_depth=3),
  AddValidationRules([NoSchemaIntrospectionCustomRule])
]

# if in debug mode.
debug = environ.get('DEBUG').lower()
if debug == 'true':
  extensions = [
    QueryDepthLimiter(max_depth=3),
  ]

# Create out schema.
schema = Schema(
                query=BaseQuery, 
                config=StrawberryConfig(auto_camel_case=False),
                extensions=extensions,
                    )