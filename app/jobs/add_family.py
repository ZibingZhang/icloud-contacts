from app import utils
from app.contact import (
    Family,
    RelatedContact,
)
from app.jobs import BaseJob


class AddFamilyJob(BaseJob):
    def predicate(self, contact):
        return contact.first_name == "FIRST NAME" and contact.last_name == "LAST NAME"

    def mapper(self, contact):
        utils.print_name_and_company(contact)
        family = Family() if contact.notes.family is None else contact.notes.family
        inp = utils.prompt()
        if inp == "":
            return
        relation, uuid = inp.split(";")
        related_contact = self.uuids[uuid]
        name = f"{related_contact.first_name} {related_contact.last_name}"

        if relation == "brother":
            if family.brothers is None:
                family.brothers = []
            family.brothers.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "cousin":
            if family.cousins is None:
                family.cousins = []
            family.cousins.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "daughter":
            if family.daughters is None:
                family.daughters = []
            family.daughters.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "sister":
            if family.sisters is None:
                family.sisters = []
            family.sisters.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "son":
            if family.sons is None:
                family.sons = []
            family.sons.append(RelatedContact(name=name, uuid=uuid))
        elif relation == "father":
            family.father = RelatedContact(name=name, uuid=uuid)
        elif relation == "mother":
            family.mother = RelatedContact(name=name, uuid=uuid)
        else:
            raise ValueError("Invalid relation")

        contact.notes.family = family
        return contact

    @staticmethod
    def maybe_add_family(notes):
        if notes.family is None:
            notes.family = Family()
