import logging

import azure.functions as func
from GraphQLAPI.utils.scalar import Base64


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    return func.HttpResponse(
             '{"value":"test"}',
             status_code=200
        )
