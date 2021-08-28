from app import utils
from app.fields import *
from app.jobs import NotesBaseJob
from app.notes import *


class AddFamilyJob(NotesBaseJob):
    uuids = {}

    def predicate(self, contact):
        notes = utils.notes_from_contact(contact)
        uuid = notes.meta.uuid
        self.uuids[uuid] = contact
        return contact.get(FIRST_NAME) == "FIRST NAME" and contact.get(LAST_NAME) == "LAST NAME"

    def mapper(self, contact):
        print(
            f"{contact.get('firstName', ''):15s}{contact.get('lastName', ''):15s}{contact.get('companyName', '')}"
        )
        return super().mapper(contact)

    def notes_mapper(self, notes: Optional[Notes]):
        inp = utils.prompt()
        if inp == "":
            return notes
        relation, uuid = inp.split(";")
        contact = self.uuids[uuid]
        name = f"{contact.get(FIRST_NAME)} {contact.get(LAST_NAME)}"
        self.maybe_add_family(notes)
        if relation == "brother":
            if notes.family.brothers is None:
                notes.family.brothers = []
            notes.family.brothers.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "cousin":
            if notes.family.cousins is None:
                notes.family.cousins = []
            notes.family.cousins.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "daughter":
            if notes.family.daughters is None:
                notes.family.daughters = []
            notes.family.daughters.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "sister":
            if notes.family.sisters is None:
                notes.family.sisters = []
            notes.family.sisters.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "son":
            if notes.family.sons is None:
                notes.family.sons = []
            notes.family.sons.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "father":
            notes.family.father = RelatedContact(name=name, uuid=uuid)
        elif relation == "mother":
            notes.family.mother = RelatedContact(name=name, uuid=uuid)
        else:
            import sys
            sys.exit(1)
        return notes

    @staticmethod
    def maybe_add_family(notes):
        if notes.family is None:
            notes.family = Family()
