from app import utils
from app.fields import *
from app.jobs import BaseJob


class ManuallyEditCompanyJob(BaseJob):
    def predicate(self, contact):
        return False

    def mapper(self, contact):
        print(
            f'{contact.get(FIRST_NAME, ""):15s} {contact.get(LAST_NAME, ""):15s} {contact.get(COMPANY_NAME, "")}'
        )
        company_name = utils.prompt()
        if company_name == "/remove":
            contact.pop(COMPANY_NAME)
        elif company_name != "":
            contact.update({COMPANY_NAME: company_name})
        return contact
