import base64
from typing import NewType
import strawberry
 
Base64 = strawberry.scalar(
    NewType("Base64", bytes),
    serialize=lambda v: base64.b64encode(v).decode("utf-8"),
    parse_value=lambda v: base64.b64decode(v).encode("utf-8"),
)

    