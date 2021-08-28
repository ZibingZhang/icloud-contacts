from app import utils
from app.fields import *
from app.jobs import BaseJob


class AddTopLevelFieldJob(BaseJob):
    def predicate(self, contact):
        notes = utils.notes_from_contact(contact)
        return False

    def mapper(self, contact):
        return contact


def add_birthday(contact):
    utils.print_name_and_company(contact, contact.get(BIRTHDAY))
    bday = utils.prompt()
    if bday == "":
        return
    contact[BIRTHDAY] = bday


def add_last_name(contact):
    utils.print_name_and_company(contact)
    name = utils.prompt()
    if name == "":
        return
    elif name.count(";") == 1:
        first, last = name.split(";")
        contact.update({FIRST_NAME: first, LAST_NAME: last})
    elif name.count(";") == 2:
        first, nick, last = name.split(";")
        contact.update({FIRST_NAME: first, NICK_NAME: nick, LAST_NAME: last})
    else:
        contact.update({LAST_NAME: name})


def add_nick_name(contact):
    utils.print_name_and_company(contact, contact.get(NICK_NAME))
    name = utils.prompt()
    if name == "":
        return
    if ";" in name:
        first, nick = name.split(";")
        contact[FIRST_NAME] = first
        contact[NICK_NAME] = nick
    else:
        contact[NICK_NAME] = name
