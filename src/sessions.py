from termcolor import colored

from base import ObservableMixin
from utils.enums import Role


class Session(ObservableMixin):

    def __init__(self):
        super().__init__()
        self.message_list = []

    def clear(self):
        self.message_list = []

    def add_message(self, message: dict, *arg, **kwargs):
        self.message_list.append(message)
        role = Role(message["role"])
        self.notify(message, role, *arg, **kwargs)

    def add_extra_message(self, message: dict, *arg, **kwargs):
        self.notify(message, None, *arg, **kwargs)


class InteractiveSession(Session):

    def get_input(self):
        message = {
            'role': Role.USER.value,
            'content': input(
                colored('\n请输入prompt: ', 'green', force_color=True)
            )  # 在这输入第一个问题
        }
        return self.add_message(message)


class MemorySession(Session):

    @classmethod
    def from_memory(cls):
        ...

    def save_memory(self):
        ...