from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FamilyDefinition:
    father: Optional[str]
    mother: Optional[str]
    sons: Optional[List[str]]
    daughters: Optional[List[str]]
    cousins: Optional[List[str]]


@dataclass
class GroupDefinition:
    name: str
    condition: callable
