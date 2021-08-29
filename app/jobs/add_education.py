from app import utils
from app.contact import (
    Education,
    School,
)
from app.jobs import BaseJob


class AddEducationJob(BaseJob):
    school = Education()

    def predicate(self, contact):
        return contact.notes.education is None

    def mapper(self, contact):
        utils.print_name_and_company(contact)
        education = contact.notes.education
        school = utils.prompt()
        if school == "":
            return
        if education is None:
            education = Education()
        if ";" in school:
            name, year = school.split(";")
            education.bachelor = School(name=name, grad_year=int(year))
        else:
            education.bachelor = School(name=school)
        contact.notes.education = education
        return contact
