from app.jobs import *
from app.cilent import ContactsClient


if __name__ == "__main__":
    client = ContactsClient()
    job = ScratchJob(client)
    job.run(preview=True)
    client.save("contacts/contacts.txt")
