def strip_for_reading(contact):
    stripped_contact = dict(contact)
    for field in {
        "isGuardianApproved",
        "contactId",
        "normalized",
        "etag",
        "whitelisted",
        "isCompany",
    }:
        stripped_contact.pop(field, None)
    return stripped_contact
