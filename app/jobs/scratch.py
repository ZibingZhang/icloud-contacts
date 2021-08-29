from app.jobs import BaseJob


class ScratchJob(BaseJob):
    def predicate(self, contact):
        return False

    def mapper(self, contact):
        return contact
