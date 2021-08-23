import json
from app import utils
from app.notes import *
from app.jobs import NotesBaseJob


class AddFriendsFriend(NotesBaseJob):
    uuids = {}

    def predicate(self, contact):
        uuid = json.loads(contact["notes"])["~"]["uuid"]
        self.uuids[uuid] = contact
        return False

    def mapper(self, contact):
        print(utils.strip_for_reading(contact))
        return super().mapper(contact)

    def notes_mapper(self, notes: Optional[Notes]):
        uuid = input(">>> ")
        if uuid == "":
            return notes
        contact = self.uuids[uuid]
        name = f"{contact.get('firstName')} {contact.get('lastName')}"
        notes.friends_friend = FriendsFriend(name=name, uuid=uuid)
        return notes
