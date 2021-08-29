import re
import typing
from typing import Optional
from app.contact import Phone
from app.jobs import BaseJob

if typing.TYPE_CHECKING:
    from app.contact import Contact


class FormatPhoneNumberJob(BaseJob):
    space = r"[-. \xa0]?"

    US_area_code = r"\d{3}"
    US_central_office_code = r"\d{3}"
    US_line_number = r"\d{4}"

    pattern_US_1 = re.compile(
        rf"\+?(1){space}({US_area_code}){space}({US_central_office_code}){space}({US_line_number})"
    )
    pattern_US_2 = re.compile(
        rf"\+?(1){space}\(({US_area_code})\){space}({US_central_office_code}){space}({US_line_number})"
    )
    pattern_US_3 = re.compile(
        rf"(){space}({US_area_code}){space}({US_central_office_code}){space}({US_line_number})"
    )
    pattern_US_4 = re.compile(
        rf"(){space}\(({US_area_code})\){space}({US_central_office_code}){space}({US_line_number})"
    )

    pattern_BR_1 = re.compile(
        rf"\+(55){space}\((\d{{2}})\){space}(\d{{5}}){space}(\d{{4}})"
    )
    pattern_CN_1 = re.compile(
        rf"\+(86){space}(\d{{3}}){space}(\d{{4}}){space}(\d{{4}})"
    )
    pattern_TW_1 = re.compile(
        rf"\+(886){space}(\d{{3}}){space}(\d{{3}}){space}(\d{{3}})"
    )
    pattern_HK_1 = re.compile(rf"\+(852){space}(\d{{4}}){space}(\d{{4}})")
    pattern_UK_1 = re.compile(rf"\+(44){space}(\d{{4}}){space}(\d{{6}})")

    def predicate(self, contact: "Contact") -> bool:
        return contact.phones is not None

    def mapper(self, contact: "Contact") -> Optional["Contact"]:
        new_phones = []
        for phone in contact.phones or []:
            number = phone.field
            label = phone.label
            if match := (
                self.pattern_US_1.match(number)
                or self.pattern_US_2.match(number)
                or self.pattern_US_3.match(number)
                or self.pattern_US_4.match(number)
            ):
                groups = match.groups()
                country_code = groups[0] or "1"
                area_code = groups[1]
                central_office_code = groups[2]
                line_number = groups[3]
                new_phones.append(
                    Phone(
                        f"+{country_code} ({area_code}) {central_office_code}-{line_number}",
                        label,
                    )
                )
            elif match := (
                self.pattern_BR_1.match(number)
                or self.pattern_CN_1.match(number)
                or self.pattern_TW_1.match(number)
            ):
                groups = match.groups()
                country_code = groups[0]
                body_1 = groups[1]
                body_2 = groups[2]
                body_3 = groups[3]
                new_phones.append(
                    Phone(f"+{country_code} {body_1} {body_2} {body_3}", label)
                )
            elif match := (
                self.pattern_HK_1.match(number) or self.pattern_UK_1.match(number)
            ):
                groups = match.groups()
                country_code = groups[0]
                body_1 = groups[1]
                body_2 = groups[2]
                new_phones.append(
                    Phone(f"+{country_code} {body_1} {body_2}", label)
                )
            else:
                new_phones.append(phone)

        contact.phones = new_phones
        return contact
