from dataclasses import dataclass


def false_on_error(condition):
    def decorated_condition(contact):
        try:
            return condition(contact)
        except:
            return False

    return decorated_condition


@false_on_error
def group_condition(contact):
    return False


@dataclass
class GroupDefinition:
    name: str
    condition: callable
