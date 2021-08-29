from app import utils
from app.contact import (
    RelatedContact,
)
from app.jobs import BaseJob


class AddFriendsFriendJob(BaseJob):
    def predicate(self, contact):
        return False

    def mapper(self, contact):
        utils.print_name_and_company(contact)
        uuid = utils.prompt()
        if uuid == "":
            return
        friend_contact = self.uuids[uuid]
        name = f"{friend_contact.first_name} {friend_contact.last_name}"
        contact.notes.friends_friend = RelatedContact(name=name, uuid=uuid)
        return contact
