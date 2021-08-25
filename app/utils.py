import json
from app.fields import *
from app.notes import Notes


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
            notes = json.loads(notes)
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
        return json.dumps(notes, indent=2, sort_keys=True, ensure_ascii=False)
    else:
        return json.dumps(
            json.loads(notes), indent=2, sort_keys=True, ensure_ascii=False
        )


def notes_from_contact(contact):
    notes = contact.get("notes")
    notes = json.loads(notes)
    if notes.get("~"):
        notes["meta"] = notes.pop("~")
    notes = Notes.from_dict(notes)
    return notes


def prompt(msg=">>> "):
    return input(msg).strip()
