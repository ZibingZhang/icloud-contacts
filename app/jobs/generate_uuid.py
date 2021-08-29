from app import utils
from app.jobs import NotesBaseJob
from app.notes import *


class GenerateUUIDJob(NotesBaseJob):
    def predicate(self, contact):
        super().predicate(contact)
        try:
            notes = utils.notes_from_contact(contact)
            return notes.meta is None or notes.meta.uuid is None
        except KeyError:
            return True

    def notes_mapper(self, notes: Optional[Notes]):
        updated_notes = notes
        if updated_notes is None:
            updated_notes = Notes()
        updated_notes.meta = Meta(uuid=utils.generate_uuid())
        return updated_notes
