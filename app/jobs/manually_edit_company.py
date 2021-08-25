from app.jobs import BaseJob


class ManuallyEditCompanyJob(BaseJob):
    def predicate(self, contact):
        return False

    def mapper(self, contact):
        print(
            f'{contact.get("firstName", ""):15s} {contact.get("lastName", ""):15s} {contact.get("companyName", "")}'
        )
        company_name = input(">>> ").strip()
        if company_name == "/remove":
            contact.pop("companyName")
        elif company_name != "":
            contact.update({"companyName": company_name})
        return contact
