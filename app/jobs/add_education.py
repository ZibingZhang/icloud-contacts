from app import utils
from app.notes import *
from app.jobs import NotesBaseJob


class AddEducationJob(NotesBaseJob):
    school = Education()

    def predicate(self, contact):
        notes = utils.notes_from_contact(contact)
        return notes.education is None or notes.education.bachelor is None

    def mapper(self, contact):
        print(
            f"{contact.get('firstName', ''):15s}{contact.get('lastName', ''):15s}{contact.get('companyName', '')}"
        )
        return super().mapper(contact)

    def notes_mapper(self, notes: Optional[Notes]):
        school = utils.prompt()
        if school == "":
            return notes
        if notes.education is None:
            notes.education = Education()
        if ";" in school:
            name, year = school.split(";")
            notes.education.bachelor = School(name=name, grad_year=int(year))
        else:
            notes.education.bachelor = School(name=school)
        return notes
