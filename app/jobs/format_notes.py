from app.fields import *
from app.jobs import NotesBaseJob
from app.notes import *


class FormatNotesJob(NotesBaseJob):
    def predicate(self, contact):
        return contact.get(NOTES) is not None

    def notes_mapper(self, notes: Optional[Notes]):
        return notes
