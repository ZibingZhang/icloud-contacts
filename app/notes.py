from dataclasses import dataclass
from typing import List, Optional
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Education:
    major: Optional[str] = None
    school: Optional[str] = None


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Favorite:
    candy: Optional[str] = None
    color: Optional[str] = None


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
    education: Optional[List[Education]] = None
    favorite: Optional[Favorite] = None
    partner: Optional[Partner] = None
