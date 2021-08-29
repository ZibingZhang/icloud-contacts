import json
import sys
import time
from app import config
from app import utils
from app.contact import (
    Contact,
    Group,
    Meta,
    Notes,
)
from pyicloud.src import PyiCloudService


class ContactsClient:
    def __init__(self):
        self.service = self._login()
        self._contacts = []
        self._groups = []

    def contacts(self, refresh=False):
        if len(self._contacts) == 0 or refresh:
            self._refresh_contacts()
        return self._contacts

    def groups(self, refresh=False):
        if len(self._groups) == 0 or refresh:
            self._refresh_groups()
        return self._groups

    def create(self, contact):
        """
        Create a contact.
        """
        self._generate_uuid(contact)
        contact_dict = self._contact_to_dict(contact)
        self.service.create(contact_dict)

    def read(self, refresh=False):
        """
        Fetches all the contacts.
        """
        self._refresh()
        return self._contacts

    def update(self, contact):
        contact_dict = self._contact_to_dict(contact)
        self.service.update(contact_dict)

    def create_group(self, group):
        self.service.create_group(group.to_dict())

    def delete_group(self, group):
        self.service.delete_group(group.to_dict())

    def save(self, filename):
        """
        Saves all contacts to a file.
        """
        contacts = self.read()
        with open(filename, "w") as f:
            for contact in contacts:
                f.write(f"{utils.contact_to_json(contact)}\n")

    def filter_map(
        self,
        predicate,
        mapper,
        preview=False,
        delay=0.1,
        out=sys.stdout,
    ):
        """
        Updates many contacts.
        """
        filtered_contacts = list(filter(predicate, self.contacts()))
        print(
            f"You are processing {len(filtered_contacts)} contacts {'(preview)' if preview else ''}"
        )
        input("Press enter to continue...\n")
        for contact in filtered_contacts:
            old_contact = Contact.from_dict(contact.to_dict())
            updated_contact = mapper(contact)
            if updated_contact is None or old_contact == updated_contact:
                continue
            elif not preview:
                time.sleep(delay)
                self.update(updated_contact)
            out.write(
                f"Updated {utils.json_for_reading(old_contact)} to {utils.json_for_reading(updated_contact)}\n"
            )

    def _refresh(self):
        self.service.refresh()
        self._refresh_contacts()
        self._refresh_groups()

    def _refresh_contacts(self):
        self._contacts = list(map(Contact.from_dict, self.service.contacts))

    def _refresh_groups(self):
        self._groups = list(map(Group.from_dict, self.service.groups))

    @staticmethod
    def _login():
        username = config.USERNAME
        password = config.PASSWORD

        api = PyiCloudService(username, password)

        if api.requires_2fa:
            print("Two-factor authentication required.")
            code = input(
                "Enter the code you received of one of your approved devices: "
            )
            result = api.validate_2fa_code(code)
            print("Code validation result: %s" % result)

            if not result:
                print("Failed to verify security code")
                sys.exit(1)

            if not api.is_trusted_session:
                print("Session is not trusted. Requesting trust...")
                result = api.trust_session()
                print("Session trust result %s" % result)

                if not result:
                    print(
                        "Failed to request trust. You will likely be prompted for the code again in the coming weeks"
                    )
        elif api.requires_2sa:
            import click

            print("Two-step authentication required. Your trusted devices are:")

            devices = api.trusted_devices
            for i, device in enumerate(devices):
                print(
                    "  %s: %s"
                    % (
                        i,
                        device.get(
                            "deviceName", "SMS to %s" % device.get("phoneNumber")
                        ),
                    )
                )

            device = click.prompt("Which device would you like to use?", default=0)
            device = devices[device]
            if not api.send_verification_code(device):
                print("Failed to send verification code")
                sys.exit(1)

            code = click.prompt("Please enter validation code")
            if not api.validate_verification_code(device, code):
                print("Failed to verify verification code")
                sys.exit(1)

        return api.contacts

    @staticmethod
    def _contact_to_dict(contact):
        formatted_contact = contact.to_dict()
        try:
            formatted_contact.update({"notes": utils.format_notes(contact.notes)})
        except (KeyError, json.JSONDecodeError):
            pass
        return formatted_contact

    @staticmethod
    def _generate_uuid(contact):
        if contact.notes is None:
            contact.notes = Notes()
        meta = contact.notes.meta
        if meta is None:
            meta = Meta()
        if meta.uuid is None:
            meta.uuid = utils.generate_uuid()
        contact.notes.meta = meta
