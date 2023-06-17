import config
from utils.enums import Role
from base import Observer
from termcolor import colored

from utils.utils import num_tokens_from_string, num_tokens_from_messages


class Shell(Observer):

    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    def handle(self, session, message: dict, role: Role):
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
            content = message['content'][:200].replace(' ', '') + '...'
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


class SlidingWindowHandler:
    """滑动窗口，控制tk数量"""
    max_window_size = config.window_size

    def __init__(self):
        self.num_tk_list = []
        self.current_window_size = 0

    def handle(self, session, message: dict, role: Role):
        num_tokens = 0
        for key, value in message.items():
            if value:
                num_tokens += num_tokens_from_string(str(value))
        self.num_tk_list.append(num_tokens)
        self.current_window_size += num_tokens
        while 1:
            if self.current_window_size > self.max_window_size:
                # 从左开始第一个非system角色的message删掉，直到低于max_window_size
                for index, message in enumerate(session.message_list):
                    role = Role(message['role'])
                    if role is not Role.SYSTEM:
                        num_token = self.num_tk_list.pop(index)
                        session.message_list.pop(index)
                        self.current_window_size -= num_token
            else:
                break
