from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, List, Optional
from dataclasses_json import LetterCase, Undefined, dataclass_json
from dataclasses_json import config as metadata
import yaml
from app import utils


def reflect_none(fn: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def wrapped_fn(arg):
        if arg is None:
            return None
        else:
            return fn(arg)

    return wrapped_fn


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.RAISE)
@dataclass
class RelatedContact:
    name: Optional[str] = None
    uuid: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.RAISE)
@dataclass
class School:
    grad_year: Optional[int] = None
    major: Optional[str] = None
    minor: Optional[str] = None
    name: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.RAISE)
@dataclass
class Education:
    high_school: Optional[School] = None
    bachelor: Optional[School] = None
    master: Optional[School] = None


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.RAISE)
@dataclass
class Family:
    brothers: Optional[List[RelatedContact]] = None
    cousins: Optional[List[RelatedContact]] = None
    daughters: Optional[List[RelatedContact]] = None
    father: Optional[RelatedContact] = None
    mother: Optional[RelatedContact] = None
    sisters: Optional[List[RelatedContact]] = None
    sons: Optional[List[RelatedContact]] = None


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.RAISE)
@dataclass
class Favorite:
    candy: Optional[str] = None
    color: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.RAISE)
@dataclass
class Meta:
    tags: Optional[List[str]] = None
    uuid: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.RAISE)
@dataclass
class Partner:
    end: Optional[str] = None
    start: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE, undefined=Undefined.RAISE)
@dataclass
class Notes:
    chinese_name: Optional[str] = None
    comment: Optional[str] = None
    education: Optional[Education] = None
    family: Optional[Family] = None
    favorite: Optional[Favorite] = None
    friends_friend: Optional[RelatedContact] = None
    meta: Optional[Meta] = None
    partner: Optional[Partner] = None


@reflect_none
def notes_decoder(notes: str) -> Notes:
    return Notes.from_dict(yaml.safe_load(notes))


@reflect_none
def notes_encoder(notes: Notes) -> str:
    return utils.format_notes(notes)


class PhoneLabel(Enum):
    HOME = "HOME"
    HOME_FAX = "HOME FAX"
    IPHONE = "IPHONE"
    MAIN = "MAIN"
    MOBILE = "MOBILE"
    OTHER = "OTHER"
    PAGER = "PAGER"
    WORK = "WORK"
    WORK_FAX = "WORK FAX"


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class Phone:
    field: str
    label: Optional[str] = None


@reflect_none
def phones_decoder(phones: Optional[List[dict]]) -> Optional[List[Phone]]:
    return list(map(Phone.from_dict, phones))


@reflect_none
def phones_encoder(phones: List[Phone]) -> List[dict]:
    return list(map(Phone.to_dict, phones))


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.RAISE)
@dataclass
class Contact:
    prefix: Optional[str] = None
    first_name: Optional[str] = None
    phonetic_first_name: Optional[str] = None
    nick_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    phonetic_last_name: Optional[str] = None
    suffix: Optional[str] = None
    normalized: Optional[str] = None

    company_name: Optional[str] = None
    phonetic_company_name: Optional[str] = None
    department: Optional[str] = None
    job_title: Optional[str] = None

    dates: Any = None
    email_addresses: Any = None
    phones: Optional[Phone] = field(
        default=None, metadata=metadata(decoder=phones_decoder, encoder=phones_encoder)
    )
    IMs: Any = field(default=None, metadata=metadata(letter_case=LetterCase.PASCAL))
    profiles: Any = None
    related_names: Any = None
    street_addresses: Any = None
    urls: Any = None

    birthday: Optional[str] = None
    notes: Optional[Notes] = field(
        default=None, metadata=metadata(decoder=notes_decoder, encoder=notes_encoder)
    )

    contact_id: Optional[str] = None
    etag: Optional[str] = None
    is_company: bool = False
    is_guardian_approved: Optional[bool] = None
    photo: Any = None
    whitelisted: Optional[bool] = None


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.RAISE)
@dataclass
class Group:
    name: str
    group_id: Optional[str] = None
    contact_ids: List[str] = field(default_factory=list)

    etag: Optional[bool] = None
    header_positions: Any = None
    is_guardian_approved: Optional[bool] = None
    whitelisted: Optional[bool] = None
