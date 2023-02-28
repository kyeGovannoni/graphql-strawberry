import logging

import azure.functions as func
from azure.functions import AsgiMiddleware
from strawberry.asgi import GraphQL
from GraphQLAPI.schemas.root import schema
#from GraphQLAPI.utils.resolvers import get_resolvers


app = GraphQL(
    schema = schema
    ) 

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)