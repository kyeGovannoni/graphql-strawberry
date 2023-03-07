import strawberry
from strawberry.schema_directive import Location
from enum import Enum

@strawberry.schema_directive(locations=[Location.OBJECT])
class Keys:
    fields: str

@strawberry.enum
class Role(Enum):
     ADMIN = 'ADMIN'
     REVIEWER = 'REVIEWER'
     USER = 'USER'
     UNKNOWN = 'UNKNOWN'


@strawberry.schema_directive(locations=[Location.OBJECT])
class Auth:
    role: Role = 'UNKNOWN'
