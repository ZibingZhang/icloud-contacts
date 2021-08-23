from app import utils
from app.jobs import BaseJob


class AddLastNameJob(BaseJob):
    @staticmethod
    def predicate(contact):
        return contact.get("lastName") is None

    @staticmethod
    def mapper(contact):
        print(utils.strip_for_reading(contact))
        name = input("")
        if name == "":
            return contact
        elif name.count(";") == 1:
            first, last = name.split(";")
            contact.update({"firstName": first, "lastName": last})
        elif name.count(";") == 2:
            first, nick, last = name.split(";")
            contact.update({"firstName": first, "nickName": nick, "lastName": last})
        else:
            contact.update({"lastName": name})
        return contact
