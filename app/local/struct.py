from dataclasses import dataclass


@dataclass
class GroupDefinition:
    name: str
    condition: callable
