from itertools import islice
import pyodbc, struct
import typing
from os import environ

def get_connection_string() -> str:
    if environ.get('CONNECT_VIA_LOGIN').lower() == 'true':
        return 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:%s,1433;Database=%s;Uid=%s;Pwd=%s;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30' %(
            environ.get('SERVERLESS_SERVER'),
            environ.get('SERVERLESS_DATABASE'),
            environ.get('SERVERLESS_USERNAME'),
            environ.get('SERVERLESS_PASSWORD'),
        )
    else:
        return 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:%s,1433;Database=%s;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30' %(
            environ.get('SERVERLESS_SERVER'),
            environ.get('SERVERLESS_DATABASE')
        )

def add_pyodbc_for_access_token(credentials, kwargs:typing.Optional[dict] = None) -> dict:
    kwargs = kwargs or {}
    if (credentials) and environ.get('CONNECT_VIA_LOGIN').lower() == 'false':
        token = credentials.get_token()
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        token_struct = struct.pack(f'<I{len(token)}s', len(token), token)
        kwargs = {"attrs_before": {SQL_COPT_SS_ACCESS_TOKEN: token_struct}}
    return kwargs

def get_sql_data(sql_statement:str , parameters:str, connection_string:str, kwargs:dict ) -> dict:
    with pyodbc.connect(connection_string, **kwargs) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_statement, *parameters)
            columns = [desc[0] for desc in cursor.description]
            rows = [] 
            row = cursor.fetchone()
            rows.append(row)

            while row:
                row = cursor.fetchone()
                if row:
                    rows.append(row)

    data = [dict(zip(columns, row)) for row in rows]
    return data