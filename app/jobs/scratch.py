from app.notes import *
from app.jobs import BaseJob, NotesBaseJob


class ScratchJob(BaseJob):
    def predicate(self, contact):
        return True

    def mapper(self, contact):
        return contact


class ScratchNotesJob(NotesBaseJob):
    def predicate(self, contact):
        return True

    def notes_mapper(self, notes: Optional[Notes]):
        return notes