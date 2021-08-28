from dataclasses import dataclass
from typing import List, Optional
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class RelatedContact:
    name: Optional[str] = None
    uuid: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class School:
    grad_year: Optional[int] = None
    major: Optional[str] = None
    minor: Optional[str] = None
    name: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Education:
    high_school: Optional[School] = None
    bachelor: Optional[School] = None
    master: Optional[School] = None


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Family:
    brothers: Optional[List[RelatedContact]] = None
    cousins: Optional[List[RelatedContact]] = None
    daughters: Optional[List[RelatedContact]] = None
    father: Optional[RelatedContact] = None
    mother: Optional[RelatedContact] = None
    sisters: Optional[List[RelatedContact]] = None
    sons: Optional[List[RelatedContact]] = None


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Favorite:
    candy: Optional[str] = None
    color: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Meta:
    uuid: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Partner:
    end: Optional[str] = None
    start: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE)
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
