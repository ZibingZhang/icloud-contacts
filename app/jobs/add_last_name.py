from app import utils
from app.fields import *
from app.jobs import BaseJob


class AddLastNameJob(BaseJob):
    def predicate(self, contact):
        return contact.get(LAST_NAME) is None

    def mapper(self, contact):
        print(utils.strip_for_reading(contact))
        name = utils.prompt()
        if name == "":
            return contact
        elif name.count(";") == 1:
            first, last = name.split(";")
            contact.update({FIRST_NAME: first, LAST_NAME: last})
        elif name.count(";") == 2:
            first, nick, last = name.split(";")
            contact.update({FIRST_NAME: first, NICK_NAME: nick, LAST_NAME: last})
        else:
            contact.update({LAST_NAME: name})
        return contact
