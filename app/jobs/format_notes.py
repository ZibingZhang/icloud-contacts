from app.notes import *
from app.jobs import NotesBaseJob


class FormatNotesJob(NotesBaseJob):
    def predicate(self, contact):
        return contact.get("notes") is not None

    def notes_mapper(self, notes: Optional[Notes]):
        return notes
