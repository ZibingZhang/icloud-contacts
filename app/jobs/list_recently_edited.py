from pprint import pprint
from app.jobs import BaseJob


class ListRecentlyEditedJob(BaseJob):
    def run(self, preview: bool = True) -> None:
        contacts = {}
        for contact in self.client.contacts():
            edit_id = int(contact.etag[2:6])
            contacts[edit_id] = contact
        pprint(contacts)
