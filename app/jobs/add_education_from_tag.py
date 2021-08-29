from app.contact import *
from app.jobs import BaseJob


class AddEducationFromTagJob(BaseJob):
    school = Education()

    def predicate(self, contact):
        return any(
            map(lambda tag: "SCHOOL" in tag, contact.company_name.split(", "))
        )

    def mapper(self, contact):
        utils.print_name_and_company(contact)
        contact.notes.education = Education()
        return contact
