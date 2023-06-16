from utils.enums import Role
from base import Observer
from termcolor import colored


class Shell(Observer):

    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    def handle(self, message: dict, role: Role):
        if role is Role.SYSTEM:
            formatted_message = f"[system]: {message['content']}"
        elif role is Role.USER:
            formatted_message = f"[user]: {message['content']}"
        elif role is Role.ASSISTANT and message.get("function_call"):
            # "判断用工具可用
            func_call = message['function_call']
            formatted_message = f"[assistant] ({func_call['name']}): {str(func_call['arguments'])}"
        elif role is Role.ASSISTANT and not message.get("function_call"):
            formatted_message = f"[assistant]: {message['content']}"
        elif role is Role.FUNCTION:
            content = message['content'][:100].replace(' ', '') + '...'
            formatted_message = f"[function] ({message['name']}): {content}"
        elif role is None:
            formatted_message = f'异常message: {message}'
        else:
            formatted_message = f'异常message: {message}'
        print(
            colored(
                formatted_message,
                self.role_to_color[role],
                force_color=True
            )
        )

