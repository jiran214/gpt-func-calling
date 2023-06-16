import json
import os

from typing import Iterable, Dict, List, Type

import openai

import config
from tenacity import retry, wait_random_exponential, stop_after_attempt
from enums import Role
from session import Session
from base import ToolModel

openai.api_key = config.api_key
os.environ["http_proxy"] = f'http://{config.proxy}/'
os.environ["https_proxy"] = f'http://{config.proxy}/'


class GPTAgent:

    def __init__(self, tool_map: Dict[str, Type[ToolModel]], functions: List[dict], session: Session):
        self.tool_map = tool_map
        self.functions = functions
        self.function_call = "auto"
        self.model = "gpt-3.5-turbo-0613"
        self.session = session

    @classmethod
    def from_tools(cls, tools: Iterable[Type[ToolModel]], session: Session):
        tool_map = {}
        gpt_schema_list = []
        for tool in tools:
            tool_map[tool.Meta.name] = tool
            gpt_schema_list.append(tool.gpt_schema())
        return cls(
            tool_map=tool_map,
            functions=gpt_schema_list,
            session=session
        )

    @retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
    def _generate(self):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.session.message_list,
                functions=self.functions,
                function_call=self.function_call,
            )
            return response
        except Exception as e:
            raise e

    def run(self):
        # Step 1, send model the user query and what functions it has access to
        response = self._generate()
        message = response["choices"][0]["message"]
        self.session.add_message(message)

        # Step 2, check if the model wants to call a function
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            function_args = json.loads(message["function_call"]["arguments"])

            if function_name not in self.tool_map:
                raise 'tool_map key 不等于 Meta name'

            # Step 3, call the function
            tool = self.tool_map[function_name](**function_args)
            function_response = tool.use()
            # Step 4, send model the info on the function call and function response
            message = {
                "role": Role.FUNCTION.value,
                "name": function_name,
                "content": function_response,
            }
            self.session.add_message(message)
            second_response = self._generate()
            self.session.add_message(second_response["choices"][0]["message"])