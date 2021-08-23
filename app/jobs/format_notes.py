from typing import Optional
from app.notes import Notes
from app.jobs import NotesBaseJob


class FormatNotesJob(NotesBaseJob):
    @staticmethod
    def predicate(contact):
        return contact.get("notes") is not None

    def notes_mapper(self, notes: Optional[Notes]):
        return notes
