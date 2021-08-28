from app import utils
from app.fields import *
from app.notes import *
from app.jobs import BaseJob, NotesBaseJob


class ScratchJob(BaseJob):
    def predicate(self, contact):
        return False

    def mapper(self, contact):
        return contact


class ScratchNotesJob(NotesBaseJob):
    def predicate(self, contact):
        notes = utils.notes_from_contact(contact)
        return True

    def notes_mapper(self, notes: Optional[Notes]):
        return notes
