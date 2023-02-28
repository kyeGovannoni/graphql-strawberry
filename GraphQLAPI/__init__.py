import logging

import azure.functions as func
from azure.functions import AsgiMiddleware
from GraphQLAPI.models.schema import schema
from GraphQLAPI.utils.app_extension import MyGrapQL

# credentials = DefaultAzureCredential()
# credentials = DefaultAzureCredential()
# conn_string = get_connection_string()
# conn_kwargs = add_pyodbc_for_access_token(credentials)

app = MyGrapQL(
    schema = schema,
    credentials=None
    ) 

async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return await AsgiMiddleware(app).handle_async(req, context)