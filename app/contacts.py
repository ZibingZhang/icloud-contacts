import json
import sys
import time
from app import utils
from app.login import contacts_login


class ContactsClient:
    def __init__(self):
        self.contacts_service = contacts_login()

    def all(self):
        """
        Fetches all the contacts.
        """
        self.contacts_service.refresh_contacts()
        return self.contacts_service.contacts

    def save(self, filename):
        """
        Saves all contacts to a file.
        """
        contacts = self.all()
        with open(filename, "w") as f:
            for contact in contacts:
                f.write(f"{json.dumps(contact)}\n")

    def filter_map(self, predicate, mapper, preview=False, delay=0.1, out=sys.stdout):
        """
        Updates many contacts.
        """
        self.contacts_service.refresh_contacts()
        self.contacts_service.refresh_tokens()
        filtered_contacts = list(filter(predicate, self.contacts_service.contacts))
        print(
            f"You are processing {len(filtered_contacts)} contacts {'(preview)' if preview else ''}"
        )
        input("Press enter to continue...\n")
        for contact in filtered_contacts:
            old_contact = dict(contact)
            updated_contact = mapper(contact)
            if old_contact == updated_contact:
                continue
            elif not preview:
                time.sleep(delay)
                self.contacts_service.set(updated_contact)
            out.write(
                f"Updated {utils.strip_for_reading(old_contact)} to {utils.strip_for_reading(updated_contact)}\n"
            )
