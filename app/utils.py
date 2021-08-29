import json
import uuid
import yaml
from app import utils
from app.fields import *
from app.notes import *


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


def strip_for_reading(contact):
    stripped_contact = dict(contact)
    for field in {
        CONTACT_ID,
        E_TAG,
        IS_COMPANY,
        IS_GUARDIAN_APPROVED,
        NORMALIZED,
        WHITELISTED,
    }:
        stripped_contact.pop(field, None)
    try:
        notes = contact["notes"]
        if not isinstance(notes, dict):
            notes = dict(yaml.safe_load(notes))
        stripped_contact["notes"] = json.dumps(notes, ensure_ascii=False)
    except (KeyError, json.JSONDecodeError):
        pass
    return stripped_contact


# https://stackoverflow.com/questions/33797126/proper-way-to-remove-keys-in-dictionary-with-none-values-in-python
def delete_none(dict_):
    for key, value in list(dict_.items()):
        if isinstance(value, dict):
            delete_none(value)
        elif value is None:
            del dict_[key]
        elif isinstance(value, list):
            for v_i in value:
                delete_none(v_i)
    return dict_


def format_notes(notes):
    if isinstance(notes, dict):
        notes_dict = dict(notes)
    elif isinstance(notes, Notes):
        notes_dict = notes.to_dict()
    else:
        notes_dict = json.loads(notes)
    notes_dict = delete_none(notes_dict)

    try:
        notes_meta = notes_dict.pop("meta")
    except KeyError:
        notes_meta = None

    if len(notes_dict.keys()) == 0:
        output = ""
    else:
        notes_json = json.dumps(utils.delete_none(notes_dict), ensure_ascii=False)
        output = json_to_yaml(notes_json)

    if notes_meta is not None:
        notes_meta_json = json.dumps(
            {"meta": utils.delete_none(notes_meta)}, ensure_ascii=False
        )
        output += json_to_yaml(notes_meta_json)

    return output


def notes_from_contact(contact):
    return Notes.from_dict(yaml.safe_load(contact.get("notes")))


def prompt(msg=">>> "):
    return input(msg).strip()


def json_to_yaml(json_):
    return yaml.dump(
        yaml.safe_load(json_),
        allow_unicode=True,
        indent=4,
        # Dumper=Dumper,
    )


def print_name_and_company(contact, more=""):
    print(
        f'{contact.get(FIRST_NAME, ""):15s}{contact.get(LAST_NAME, ""):15s}{contact.get(COMPANY_NAME, ""):30s}{more}'
    )


def generate_uuid():
    return str(uuid.uuid4())[:13]
