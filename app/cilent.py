import json
import sys
import time
from app import utils
from app.fields import *
from app.notes import *
from pyicloud.src import PyiCloudService


class ContactsClient:
    def __init__(self):
        self.contacts_service = self._login()

    def create(self, contact):
        """
        Create a contact.
        """
        self._generate_uuid(contact)
        self._set_required_fields(contact)
        formatted_contact = self._format_notes(contact)
        self.contacts_service.create(formatted_contact)

    def read(self):
        """
        Fetches all the contacts.
        """
        self.contacts_service.refresh_contacts()
        return self.contacts_service.contacts

    def update(self, contact):
        formatted_contact = self._format_notes(contact)
        self.contacts_service.update(formatted_contact)

    def save(self, filename):
        """
        Saves all contacts to a file.
        """
        contacts = self.read()
        with open(filename, "w") as f:
            for contact in contacts:
                f.write(f"{json.dumps(contact)}\n")

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
            if updated_contact is None or old_contact == updated_contact:
                continue
            elif not preview:
                time.sleep(delay)
                self.update(updated_contact)
            out.write(
                f"Updated {utils.strip_for_reading(old_contact)} to {utils.strip_for_reading(updated_contact)}\n"
            )

    @staticmethod
    def _login():
        with open("config.json") as f:
            config = json.load(f)
        username = config["username"]
        password = config["password"]

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
    def _format_notes(contact):
        formatted_contact = dict(contact)
        try:
            formatted_contact.update({"notes": utils.format_notes(contact["notes"])})
        except (KeyError, json.JSONDecodeError):
            pass
        return formatted_contact

    @staticmethod
    def _generate_uuid(contact):
        notes = contact.get(NOTES, Notes())
        if notes.meta is None:
            notes.meta = Meta()
        if notes.meta.uuid is None:
            notes.meta.uuid = utils.generate_uuid()
        contact[NOTES] = notes

    @staticmethod
    def _set_required_fields(contact):
        contact[IS_COMPANY] = False
