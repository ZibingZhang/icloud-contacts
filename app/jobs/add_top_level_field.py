import typing
from typing import Optional
from app import utils
from app.jobs import BaseJob

if typing.TYPE_CHECKING:
    from app.contact import Contact


class AddTopLevelFieldJob(BaseJob):
    def predicate(self, contact: "Contact") -> bool:
        return False

    def mapper(self, contact: "Contact") -> Optional["Contact"]:
        return contact


def add_birthday(contact: "Contact") -> None:
    utils.print_name_and_company(contact, contact.birthday)
    birthday = utils.prompt()
    if birthday == "":
        return
    contact.birthday = birthday


def add_last_name(contact: "Contact") -> None:
    utils.print_name_and_company(contact)
    name = utils.prompt()
    if name == "":
        return
    elif name.count(";") == 1:
        first, last = name.split(";")
        contact.first_name = first
        contact.last_name = last
    elif name.count(";") == 2:
        first, nick, last = name.split(";")
        contact.first_name = first
        contact.nick_name = nick
        contact.last_name = last
    else:
        contact.last_name = name


def add_nick_name(contact: "Contact") -> None:
    utils.print_name_and_company(contact, contact.nick_name)
    name = utils.prompt()
    if name == "":
        return
    if ";" in name:
        first, nick = name.split(";")
        contact.first_name = first
        contact.nick_name = nick
    else:
        contact.nick_name = name
