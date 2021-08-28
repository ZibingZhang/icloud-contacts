from app import utils
from app.fields import *
from app.jobs import NotesBaseJob
from app.notes import *


class AddFriendsFriendJob(NotesBaseJob):
    def predicate(self, contact):
        return False

    def mapper(self, contact):
        print(utils.strip_for_reading(contact))
        return super().mapper(contact)

    def notes_mapper(self, notes: Optional[Notes]):
        uuid = utils.prompt()
        if uuid == "":
            return notes
        contact = self.uuids[uuid]
        name = f"{contact.get(FIRST_NAME)} {contact.get(LAST_NAME)}"
        notes.friends_friend = RelatedContact(name=name, uuid=uuid)
        return notes
