if __name__ == "__main__":
    from app.login import contacts_login

    tags = set()
    api = contacts_login()
    contacts = api.all()
    for contact in contacts:
        if contact_tags := contact.get("companyName"):
            for tag in contact_tags.split(", "):
                tags.add(tag)
    for tag in tags:
        print(tag)
