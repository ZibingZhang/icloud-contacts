import abc
from typing import Optional, Any
from app import utils
from app.notes import Notes


class JobMeta(type):
    # https://stackoverflow.com/questions/44029167/how-to-run-a-method-before-after-all-class-function-calls-with-arguments-passed/
    # https://stackoverflow.com/questions/392160/what-are-some-concrete-use-cases-for-metaclasses
    def __new__(mcs, name, bases, dct) -> Any:
        def wrap_run(fn):
            def enhanced_run(self, *args, **kwargs):
                getattr(self, "before_run")(self, *args, **kwargs)
                result = fn(self, *args, **kwargs)
                getattr(self, "after_run")(self, *args, **kwargs)
                return result

            return enhanced_run

        if "run" in dct:
            dct["before_run"] = JobMeta._get_required_method("before_run", bases, dct)
            dct["after_run"] = JobMeta._get_required_method("after_run", bases, dct)
            dct["run"] = wrap_run(dct["run"])

        return super().__new__(mcs, name, bases, dct)

    @staticmethod
    def _get_required_method(name, bases, dct):
        fn = None
        if name in dct:
            fn = dct[name]
        else:
            for base in bases:
                base_dir = dir(base)
                if name in base_dir:
                    fn = getattr(base, name)
                    break
        if fn is None or not callable(fn):
            raise ValueError(f"Expected method definition with name {name}")
        return fn


class BaseJob(metaclass=JobMeta):
    def __init__(self, client):
        self.uuids = {}
        self.client = client

    def run(self, preview=True):
        self.client.filter_map(self.predicate, self.mapper, preview=preview)

    def before_run(self, *args, **kwargs):
        contacts = self.client.all()
        for contact in contacts:
            notes = utils.notes_from_contact(contact)
            uuid = notes.meta.uuid
            self.uuids[uuid] = contact

    def after_run(self, *args, **kwargs):
        pass

    def predicate(self, contact):
        return False

    def mapper(self, contact):
        return contact


class NotesBaseJob(BaseJob):
    def mapper(self, contact):
        notes = utils.notes_from_contact(contact)
        updated_notes = self.notes_mapper(notes)
        if updated_notes is not None:
            updated_notes = updated_notes.to_dict()
            contact.update(
                {"notes": utils.format_notes(utils.delete_none(updated_notes))}
            )
        return contact

    @abc.abstractmethod
    def notes_mapper(self, notes: Optional[Notes]):
        pass


from app.jobs.scratch import ScratchJob, ScratchNotesJob
from app.jobs.add_education import AddEducationJob
from app.jobs.add_education_from_tag import AddEducationFromTagJob
from app.jobs.add_family import AddFamilyJob
from app.jobs.add_friends_friend import AddFriendsFriendJob
from app.jobs.add_last_name import AddLastNameJob
from app.jobs.format_notes import FormatNotesJob
from app.jobs.generate_uuid import GenerateUUIDJob
from app.jobs.manually_edit_company import ManuallyEditCompanyJob
