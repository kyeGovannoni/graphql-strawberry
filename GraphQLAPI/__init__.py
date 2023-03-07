import logging
import json
import base64
import azure.functions as func
from azure.functions import AsgiMiddleware
from GraphQLAPI.models.schema import schema
from GraphQLAPI.utils.app_extension import MyGrapQL
from GraphQLAPI.utils.permissions import validate_claim_roles, Roles
# credentials = DefaultAzureCredential()
# credentials = DefaultAzureCredential()
# conn_string = get_connection_string()
# conn_kwargs = add_pyodbc_for_access_token(credentials)

app = MyGrapQL(
    schema = schema
    ) 

async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        clientPrincipal = req.headers.get('X-MS-CLIENT-PRINCIPAL')
        clientPrincipal = json.loads(base64.b64decode(clientPrincipal).decode('utf-8'))
        claim_roles = [claim['val'] for claim in clientPrincipal["claims"] if claim["typ"] == "roles"]
        
        #validate to see if claim roles match against expected roles.
        app_roles = validate_claim_roles(claim_roles, Roles) 
        if not app_roles:
            pass #return func.HttpResponse('Not authorized', status_code=401)
    except Exception:
        app_roles = [Roles('film.reader')]#return func.HttpResponse('Not authorized', status_code=401)

    app.roles = app_roles
    return await AsgiMiddleware(app).handle_async(req, context)
