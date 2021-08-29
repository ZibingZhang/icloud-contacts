from dataclasses import dataclass
from typing import Callable
import typing

if typing.TYPE_CHECKING:
    from app.contact import Contact


def false_on_error(
    condition: Callable[["Contact"], bool]
) -> Callable[["Contact"], bool]:
    def decorated_condition(contact: "Contact") -> bool:
        try:
            return condition(contact)
        except:
            return False

    return decorated_condition


@false_on_error
def group_condition(contact: "Contact") -> bool:
    return False


@dataclass
class GroupDefinition:
    name: str
    condition: callable
