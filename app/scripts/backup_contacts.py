if __name__ == "__main__":
    from datetime import datetime

    time = datetime.now().isoformat().replace(":", "-")
    with open(f"../contacts/{time}.backup.contacts.txt", "w") as backup:
        with open("../contacts/contacts.txt", "r") as contacts:
            backup.writelines(contacts.readlines())
