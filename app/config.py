from typing import List
from app.groups import (
    GroupDefinition,
    group_condition,
)
from app.local.group_conditions import *

# Login information
USERNAME: str = "username"
PASSWORD: str = "password"

# Group definitions
GROUP_DEFINITIONS: List[GroupDefinition] = [
    GroupDefinition("Group Name", group_condition),
]
