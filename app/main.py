from app.jobs import *
from app.contacts import ContactsClient


if __name__ == "__main__":
    client = ContactsClient()
    job = ScratchJob()
    job.run(client, preview=False)
    client.save("contacts.txt")
