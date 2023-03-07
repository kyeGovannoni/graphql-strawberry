from strawberry.permission import BasePermission
from strawberry.types import Info
from starlette.websockets import WebSocket
from starlette.requests import Request
from typing import Union, Any
from enum import Enum 


class IsAuthorized(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request_roles: Union[Request, WebSocket] = info.context["roles"]
        field = info.field_name
                
        if not request_roles:
            return False
        
        for role in request_roles:
            if field in Roles.role_mapping()[role]:
                return True
            
        return False

class Roles(Enum):
    # permissions based on data Models.
    BASE64_READER = 'base64.reader'
    EMPLOYEE_READER = 'employee.reader'
    TAXI_READER = 'taxi.reader'
    FILM_READER = 'film.reader'

    # permission based on granular types as example. 
    ACTOR_READER = 'actor.reader'

    # department based roles
    @classmethod
    def role_mapping(cls):
        return {
            cls.BASE64_READER: ['base64'],
            cls.EMPLOYEE_READER: [],
            cls.TAXI_READER: [],
            cls.FILM_READER: ['getAllFilms', 'getActor', 'getActors'],
            cls.ACTOR_READER: ['getActor', 'getActors', ] 
        }

def validate_claim_roles(roles:list, enum_roles:Enum = Roles):
    enum_roles = [] 
    for role in roles:
        try:
            er = Roles(role)
            enum_roles.append(er)
        except ValueError:
            pass
    if enum_roles: return set(enum_roles)


