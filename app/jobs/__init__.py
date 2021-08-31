from typing import Any, Dict, List, Optional, Tuple
import typing
from app import utils

if typing.TYPE_CHECKING:
    from app.cilent import ContactsClient
    from app.contact import Contact


class JobMeta(type):
    # https://stackoverflow.com/questions/44029167/how-to-run-a-method-before-after-all-class-function-calls-with-arguments-passed/
    # https://stackoverflow.com/questions/392160/what-are-some-concrete-use-cases-for-metaclasses
    def __new__(mcs, name: str, bases: Tuple[type], dct: dict) -> type:
        if "predicate" in dct:
            dct["predicate"] = utils.false_on_error(dct["predicate"])
        if "run" in dct:
            dct["before_run"] = JobMeta._get_required_method("before_run", bases, dct)
            dct["after_run"] = JobMeta._get_required_method("after_run", bases, dct)
            dct["run"] = JobMeta._wrap_run(dct["run"])

        return super().__new__(mcs, name, bases, dct)

    @staticmethod
    def _wrap_run(run: callable) -> callable:
        def enhanced_run(self, *args, **kwargs):
            getattr(self, "before_run")(self, *args, **kwargs)
            result = run(self, *args, **kwargs)
            getattr(self, "after_run")(self, *args, **kwargs)
            return result

        return enhanced_run

    @staticmethod
    def _get_required_method(name: str, bases: Tuple[type], dct: dict) -> callable:
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
    def __init__(self, client: "ContactsClient") -> None:
        self.uuids = {}
        self.client = client

    def run(self, preview: bool = True) -> Any:
        self.client.filter_map(self.predicate, self.mapper, preview=preview)

    def before_run(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Any:
        for contact in self.client.contacts():
            uuid = contact.notes.meta.uuid
            self.uuids[uuid] = contact

    def after_run(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Any:
        pass

    def predicate(self, contact: "Contact") -> bool:
        return False

    def mapper(self, contact: "Contact") -> Optional["Contact"]:
        pass


from app.jobs.add_education import AddEducationJob
from app.jobs.add_education_from_tag import AddEducationFromTagJob
from app.jobs.add_friends_friend import AddFriendsFriendJob
from app.jobs.add_top_level_field import AddTopLevelFieldJob
from app.jobs.format_phone_numbers import FormatPhoneNumberJob
from app.jobs.format_notes import FormatNotesJob
from app.jobs.generate_uuid import GenerateUUIDJob
from app.jobs.list_recently_edited import ListRecentlyEditedJob
from app.jobs.manually_edit_company import ManuallyEditCompanyJob
from app.jobs.scratch import ScratchJob
from app.jobs.sync_families import SyncFamilyJob
from app.jobs.sync_groups import SyncGroupsJob
