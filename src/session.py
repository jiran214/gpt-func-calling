from base import ObservableMixin


class Session(ObservableMixin):

    def __init__(self):
        super().__init__()
        self.message_list = []

    @classmethod
    def from_memory(cls):
        ...

    def add_message(self, message: dict):
        self.message_list.append(message)
        self.notify(message)
