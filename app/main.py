from app.jobs import *
from app.login import contacts_login


job = AddLastName()


if __name__ == "__main__":
    api = contacts_login()
    api.filter_map(job.predicate, job.mapper, preview=True)
    api.save("contacts.txt")
