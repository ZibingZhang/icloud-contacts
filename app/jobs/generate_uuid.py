from app import utils
from app.contact import (
    Meta,
    Notes,
)
from app.jobs import BaseJob


class GenerateUUIDJob(BaseJob):
    def predicate(self, contact):
        try:
            return contact.notes.meta.uuid is None
        except AttributeError:
            return True

    def mapper(self, contact):
        updated_notes = contact.notes
        if updated_notes is None:
            updated_notes = Notes()
        if updated_notes.meta is None:
            updated_notes.meta = Meta()
        updated_notes.meta.uuid = utils.generate_uuid()
        contact.notes = updated_notes
        return contact
