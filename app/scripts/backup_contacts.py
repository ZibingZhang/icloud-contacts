if __name__ == "__main__":
    with open("../backup.contacts.txt", "w") as backup:
        with open("../contacts.txt", "r") as contacts:
            backup.writelines(contacts.readlines())
