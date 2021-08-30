from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FamilyDefinition:
    father: Optional[str] = None
    mother: Optional[str] = None
    sons: Optional[List[str]] = None
    daughters: Optional[List[str]] = None
    cousins: Optional[List[str]] = None


@dataclass
class GroupDefinition:
    name: str
    condition: callable
