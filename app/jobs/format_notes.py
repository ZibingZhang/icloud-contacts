from app.jobs import BaseJob


class FormatNotesJob(BaseJob):
    def predicate(self, contact):
        return contact.notes is not None

    def mapper(self, contact):
        return contact
