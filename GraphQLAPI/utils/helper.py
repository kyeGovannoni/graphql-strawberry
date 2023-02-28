import typing

def data_to_schema_object(schema_object, data:None|typing.List[dict], singleton:bool):
    if not data: return   
    if singleton: 
        return [schema_object(**item) for item in data][0]
    return [schema_object(**item) for item in data]
