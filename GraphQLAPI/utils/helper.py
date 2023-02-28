import typing

def data_to_schema_object(schema_object, data:typing.List[dict], singleton:bool):
    if singleton: 
        return [schema_object(**item) for item in data][0]
    return [schema_object(**item) for item in data]
