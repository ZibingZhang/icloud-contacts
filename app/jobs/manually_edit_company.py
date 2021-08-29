import typing
from typing import Optional
from app import utils
from app.jobs import BaseJob

if typing.TYPE_CHECKING:
    from app.contact import Contact


class ManuallyEditCompanyJob(BaseJob):
    def predicate(self, contact: "Contact") -> bool:
        return False

    def mapper(self, contact: "Contact") -> Optional["Contact"]:
        utils.print_name_and_company(contact)
        company_name = utils.prompt()
        if company_name == "/remove":
            contact.company_name = None
        elif company_name != "":
            contact.company_name = company_name
        return contact
