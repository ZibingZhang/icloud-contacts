from typing import List
import typing
from app.local import group_definitions

if typing.TYPE_CHECKING:
    from app.groups import GroupDefinition

# Login information
USERNAME: str = "username"
PASSWORD: str = "password"

# Group definitions
GROUP_DEFINITIONS: List["GroupDefinition"] = group_definitions.GROUP_DEFINITIONS
