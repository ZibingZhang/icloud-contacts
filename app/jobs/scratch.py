import typing
from typing import Optional
from app.jobs import BaseJob

if typing.TYPE_CHECKING:
    from app.contact import Contact


class ScratchJob(BaseJob):
    def predicate(self, contact: "Contact") -> bool:
        return False

    def mapper(self, contact: "Contact") -> Optional["Contact"]:
        return contact
