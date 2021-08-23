import json
import uuid
from app.jobs import NotesBaseJob
from app.notes import *


class GenerateUUIDJob(NotesBaseJob):
    def predicate(self, contact):
        super().predicate(contact)
        try:
            return json.loads(contact["notes"])["~"]["uuid"] is None
        except KeyError:
            return True

    def notes_mapper(self, notes: Optional[Notes]):
        updated_notes = notes
        if updated_notes is None:
            updated_notes = Notes()
        updated_notes.meta = Meta(uuid=str(uuid.uuid4())[:13])
        return updated_notes
