import typing
from typing import Optional
from app import utils
from app.contact import Meta, Notes
from app.jobs import BaseJob

if typing.TYPE_CHECKING:
    from app.contact import Contact


class GenerateUUIDJob(BaseJob):
    def predicate(self, contact: "Contact") -> bool:
        try:
            return contact.notes.meta.uuid is None
        except AttributeError:
            return True

    def mapper(self, contact: "Contact") -> Optional["Contact"]:
        updated_notes = contact.notes
        if updated_notes is None:
            updated_notes = Notes()
        if updated_notes.meta is None:
            updated_notes.meta = Meta()
        updated_notes.meta.uuid = utils.generate_uuid()
        contact.notes = updated_notes
        return contact
