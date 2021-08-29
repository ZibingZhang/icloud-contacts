from app import utils
from app.jobs import BaseJob


class ManuallyEditCompanyJob(BaseJob):
    def predicate(self, contact):
        return False

    def mapper(self, contact):
        utils.print_name_and_company(contact)
        company_name = utils.prompt()
        if company_name == "/remove":
            contact.company_name = None
        elif company_name != "":
            contact.company_name = company_name
        return contact
