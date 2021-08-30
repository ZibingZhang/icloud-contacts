from typing import List
import typing
from app.local import family_definitions, group_definitions

if typing.TYPE_CHECKING:
    from app.local.struct import FamilyDefinition, GroupDefinition

# Login information
USERNAME: str = "username"
PASSWORD: str = "password"

# Local definitions
FAMILY_DEFINITIONS: List["FamilyDefinition"] = family_definitions.FAMILY_DEFINITIONS
GROUP_DEFINITIONS: List["GroupDefinition"] = group_definitions.GROUP_DEFINITIONS
