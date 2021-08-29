import typing
from typing import Optional
from app import utils
from app.contact import Education
from app.jobs import BaseJob

if typing.TYPE_CHECKING:
    from app.contact import Contact


class AddEducationFromTagJob(BaseJob):
    school = Education()

    def predicate(self, contact: "Contact") -> bool:
        return any(map(lambda tag: "SCHOOL" in tag, contact.company_name.split(", ")))

    def mapper(self, contact: "Contact") -> Optional["Contact"]:
        utils.print_name_and_company(contact)
        contact.notes.education = Education()
        return contact
