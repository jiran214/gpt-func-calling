from enums import Role
from base import Observer
from termcolor import colored

class Shell(Observer):

    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    def handle(self, message: dict):
        role = Role(message["role"])
        if role is Role.SYSTEM:
            formatted_message = f"system: {message['content']}\n"
        elif role is Role.USER:
            formatted_message = f"user: {message['content']}\n"
        elif role is Role.ASSISTANT and message.get("function_call"):
            func_call = message['function_call']
            formatted_message = f"assistant ({func_call['name']}): {func_call['arguments']}\n"
        elif role is Role.ASSISTANT and not message.get("function_call"):
            formatted_message = f"assistant: {message['content']}\n"
        elif role is Role.FUNCTION:
            content = message['content'][:100].replace('\n', ' ') + '...'
            formatted_message = f"function ({message['name']}): {content}\n"
        else:
            formatted_message = f'异常message: {message}'
        print(
            colored(
                formatted_message,
                self.role_to_color[role],
                force_color=True
            )
        )

