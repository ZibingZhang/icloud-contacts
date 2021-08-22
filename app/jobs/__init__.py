import abc


class BaseJob(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def predicate(contact):
        return False

    @staticmethod
    @abc.abstractmethod
    def mapper(contact):
        return contact


from app.jobs.add_last_name import AddLastName
