import abc
from typing import Optional
from app import utils
from app.notes import Notes


class BaseJob(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def predicate(contact):
        return False

    @staticmethod
    @abc.abstractmethod
    def mapper(contact):
        return contact


class NotesBaseJob(BaseJob):
    @staticmethod
    @abc.abstractmethod
    def predicate(contact):
        pass

    def mapper(self, contact):
        notes = contact.get("notes")
        if notes is not None:
            notes = Notes.from_json(notes)
        updated_notes = self.notes_mapper(notes)
        if updated_notes is not None:
            contact.update(
                {
                    "notes": utils.format_notes(
                        utils.delete_none(updated_notes.to_dict())
                    )
                }
            )
        return contact

    @abc.abstractmethod
    def notes_mapper(self, notes: Optional[Notes]):
        pass


from app.jobs.scratch import ScratchJob
from app.jobs.add_last_name import AddLastNameJob
from app.jobs.format_notes import FormatNotesJob
