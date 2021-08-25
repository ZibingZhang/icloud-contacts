from app import utils
from app.fields import *
from app.notes import *
from app.jobs import NotesBaseJob


class AddEducationFromTagJob(NotesBaseJob):
    school = Education()

    def predicate(self, contact):
        return any(
            map(lambda tag: "SCHOOL" in tag, contact.get(COMPANY_NAME, "").split(", "))
        )

    def mapper(self, contact):
        print(utils.strip_for_reading(contact))
        return super().mapper(contact)

    def notes_mapper(self, notes: Optional[Notes]):
        notes.education = Education()
        return notes
