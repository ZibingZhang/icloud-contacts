import typing
from typing import Optional
from app.jobs import BaseJob

if typing.TYPE_CHECKING:
    from app.contact import Contact


class FormatNotesJob(BaseJob):
    def predicate(self, contact: "Contact") -> bool:
        return contact.notes is not None

    def mapper(self, contact: "Contact") -> Optional["Contact"]:
        return contact
