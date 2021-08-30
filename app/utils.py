from typing import Any, Callable, Union
import json
import typing
import uuid
import yaml

if typing.TYPE_CHECKING:
    from app.contact import Contact, Notes


# puts keys on new line with additional indentation
class Dumper(yaml.Dumper):
    last_indent = 0
    new_line = False

    def write_plain(self, text, split=True):
        if self.indent == self.last_indent:
            if self.new_line:
                self.stream.write("\n" + (self.indent - 1) * " ")
            self.new_line = not self.new_line
        else:
            self.last_indent = self.indent
            self.new_line = True
        super().write_plain(text, split)


def json_for_reading(contact: "Contact") -> dict:
    stripped_contact = delete_none(contact.to_dict())
    for field in {
        "contactId",
        "eTag",
        "isCompany",
        "isGuardianApproved",
        "normalized",
        "whitelisted",
    }:
        stripped_contact.pop(field, None)
    stripped_contact["notes"] = delete_none(contact.notes.to_dict())
    return stripped_contact


# https://stackoverflow.com/questions/33797126/proper-way-to-remove-keys-in-dictionary-with-none-values-in-python
def delete_none(dict_: dict) -> dict:
    for key, value in list(dict_.items()):
        if isinstance(value, dict):
            delete_none(value)
        elif value is None:
            del dict_[key]
        elif isinstance(value, list):
            for v_i in filter(lambda v: isinstance(v, dict), value):
                delete_none(v_i)
    return dict_


def format_notes(notes: Union[dict, "Notes"]) -> str:
    notes_dict = notes if isinstance(notes, dict) else notes.to_dict()
    notes_dict = delete_none(notes_dict)

    try:
        notes_meta = notes_dict.pop("meta")
    except KeyError:
        notes_meta = None

    if len(notes_dict.keys()) == 0:
        output = ""
    else:
        notes_json = json.dumps(delete_none(notes_dict), ensure_ascii=False)
        output = json_to_yaml(notes_json)

    if notes_meta is not None:
        notes_meta_json = json.dumps(
            {"meta": delete_none(notes_meta)}, ensure_ascii=False
        )
        output += json_to_yaml(notes_meta_json)

    return output


def prompt(msg: str = ">>> ") -> str:
    return input(msg).strip()


def json_to_yaml(json_: str) -> str:
    return yaml.dump(
        yaml.safe_load(json_),
        allow_unicode=True,
        indent=4,
        # Dumper=Dumper,
    )


def print_name_and_company(contact: "Contact", more: str = "") -> None:
    print(
        f"{str(contact.first_name):15s}{str(contact.last_name):15s}{str(contact.company_name):40s}{more}"
    )


def generate_uuid() -> str:
    return str(uuid.uuid4())[:13]


def contact_to_json(contact: "Contact") -> str:
    return json.dumps(delete_none(contact.to_dict()))


def false_on_error(
    condition: Callable[[Any], bool]
) -> Callable[[Any], bool]:
    def decorated_condition(*args, **kwargs) -> bool:
        try:
            return condition(*args, **kwargs)
        except:
            return False

    return decorated_condition
