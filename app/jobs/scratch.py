from typing import Optional

from app.notes import Notes
from app.jobs import BaseJob, NotesBaseJob


class ScratchJob(BaseJob):
    @staticmethod
    def predicate(contact):
        return True

    @staticmethod
    def mapper(contact):
        return contact


class ScratchNotesJob(NotesBaseJob):
    @staticmethod
    def predicate(contact):
        return True

    def mapper(self, contact):
        return contact

    def notes_mapper(self, notes: Optional[Notes]):
        return notes
