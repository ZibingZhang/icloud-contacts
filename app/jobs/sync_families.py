from typing import List, Optional, Union
import typing
from app import config, utils
from app.contact import Contact, Family, RelatedContact
from app.jobs import BaseJob

if typing.TYPE_CHECKING:
    from app.local.struct import FamilyDefinition


class SyncFamilyJob(BaseJob):
    def run(self, preview: bool = True) -> None:
        families = config.FAMILY_DEFINITIONS
        for family in families:
            self.process_family(family, preview=preview)

    def process_family(self, family: "FamilyDefinition", preview: bool) -> None:
        father = None
        mother = None
        sons = None
        daughters = None
        cousins = None

        if family.father:
            father = self.contact_from_name_uuid(family.father)
        if family.mother:
            mother = self.contact_from_name_uuid(family.mother)
        if family.sons:
            sons = list(map(self.contact_from_name_uuid, family.sons))
        if family.daughters:
            daughters = list(map(self.contact_from_name_uuid, family.daughters))
        if family.cousins:
            cousins = list(map(self.contact_from_name_uuid, family.cousins))

        if father:
            old_father = self.copy(father)
            father.notes.family = Family(
                sons=self.possible_to_related_contacts(sons),
                daughters=self.possible_to_related_contacts(daughters),
            )
            self.possible_set_contact(old_father, father, preview=preview)
        if mother:
            old_mother = self.copy(mother)
            mother.notes.family = Family(
                sons=self.possible_to_related_contacts(sons),
                daughters=self.possible_to_related_contacts(daughters),
            )
            self.possible_set_contact(old_mother, mother, preview=preview)
        if sons:
            for son in sons:
                old_son = self.copy(son)
                son.notes.family = Family(
                    father=self.possible_to_related_contacts(father),
                    mother=self.possible_to_related_contacts(mother),
                    brothers=self.possible_to_related_contacts(
                        list(filter(lambda s: s != son, sons)) or None
                    ),
                    sisters=self.possible_to_related_contacts(daughters),
                    cousins=self.possible_to_related_contacts(cousins)
                )
                self.possible_set_contact(old_son, son, preview=preview)
        if daughters:
            for daughter in daughters:
                old_daughter = self.copy(daughter)
                daughter.notes.family = Family(
                    father=self.possible_to_related_contacts(father),
                    mother=self.possible_to_related_contacts(mother),
                    brothers=self.possible_to_related_contacts(sons),
                    sisters=self.possible_to_related_contacts(
                        list(filter(lambda d: d != daughter, daughters)) or None
                    ),
                    cousins=self.possible_to_related_contacts(cousins)
                )
                self.possible_set_contact(old_daughter, daughter, preview=preview)

    def contact_from_name_uuid(self, name_uuid: str) -> Optional[Contact]:
        if ";" in name_uuid:
            _, uuid = name_uuid.split(";")
            for contact in self.client.contacts():
                if uuid == self.get_uuid(contact):
                    return contact
        else:
            for contact in self.client.contacts():
                if name_uuid == self.format_name(contact):
                    return contact

        raise ValueError(name_uuid)

    def possible_set_contact(
        self, old_contact: Contact, new_contact: Contact, preview: bool
    ) -> None:
        if old_contact == new_contact:
            return
        print(utils.json_for_reading(old_contact))
        print(utils.json_for_reading(new_contact))
        if not preview:
            self.client.update(new_contact)

    @staticmethod
    def possible_to_related_contacts(contacts: Optional[Union[Contact, List[Contact]]]) -> Optional[Union[RelatedContact, List[RelatedContact]]]:
        if contacts is None:
            return None
        elif isinstance(contacts, list):
            related_contacts = []
            for contact in contacts:
                related_contacts.append(RelatedContact(name=SyncFamilyJob.format_name(contact), uuid=SyncFamilyJob.get_uuid(contact)))
            return related_contacts
        else:
            return RelatedContact(
                name=SyncFamilyJob.format_name(contacts),
                uuid=SyncFamilyJob.get_uuid(contacts),
            )

    @staticmethod
    def format_name(contact: Contact) -> str:
        return f"{contact.first_name or ''} {contact.last_name or ''}".strip()

    @staticmethod
    def get_uuid(contact: Contact) -> str:
        return contact.notes.meta.uuid

    @staticmethod
    def copy(contact: Contact) -> Contact:
        return Contact.from_dict(contact.to_dict())
