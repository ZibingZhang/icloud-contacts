import abc
import json
from typing import Optional
from app import utils
from app.notes import Notes


class BaseJob(abc.ABC):
    @abc.abstractmethod
    def predicate(self, contact):
        return False

    @abc.abstractmethod
    def mapper(self, contact):
        return contact


class NotesBaseJob(BaseJob):
    @abc.abstractmethod
    def predicate(self, contact):
        return False

    def mapper(self, contact):
        notes = contact.get("notes")
        if notes is not None:
            notes = json.loads(notes)
            if notes.get("~"):
                notes["meta"] = notes.pop("~")
            notes = Notes.from_dict(notes)
        updated_notes = self.notes_mapper(notes)
        if updated_notes is not None:
            updated_notes = updated_notes.to_dict()
            if updated_notes.get("meta"):
                updated_notes["~"] = updated_notes.pop("meta")
            contact.update(
                {"notes": utils.format_notes(utils.delete_none(updated_notes))}
            )
        return contact

    @abc.abstractmethod
    def notes_mapper(self, notes: Optional[Notes]):
        pass


from app.jobs.scratch import ScratchJob
from app.jobs.add_friends_friend import AddFriendsFriend
from app.jobs.add_last_name import AddLastNameJob
from app.jobs.format_notes import FormatNotesJob
from app.jobs.generate_uuid import GenerateUUIDJob
from app.jobs.manually_edit_company import ManuallyEditCompanyJob
