from base import ObservableMixin
from utils.enums import Role


class Session(ObservableMixin):

    def __init__(self):
        super().__init__()
        self.message_list = []

    @classmethod
    def from_memory(cls):
        ...

    def add_message(self, message: dict, *arg, **kwargs):
        self.message_list.append(message)
        role = Role(message["role"])
        self.notify(message, role, *arg, **kwargs)

    def add_extra_message(self, message: dict, *arg, **kwargs):
        self.notify(message, None, *arg, **kwargs)
