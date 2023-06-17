from abc import ABC
from enum import Enum

from pydantic import BaseModel

python_type_2_json = {
    "str": "string",
    "float": "number",
    "int": "integer",
    "bool": "boolean",
    "list": "array",
    "dict": "object",
}


class ToolModel(BaseModel, ABC):

    def use(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def gpt_schema(cls, *args, **kwargs):
        cached = cls.__schema_cache__.get('function_calling_schema')
        if cached is not None:
            return cached
        model_class = cls
        properties = {}
        required = []
        for field_name, field in model_class.__fields__.items():
            properties[field_name] = {
                'type': field.type_.__name__,
                'description': field.field_info.description
            }
            if field.required:
                required.append(field_name)
            if issubclass(field.type_, Enum):
                for type_ in field.type_.mro():
                    if type_.__name__ not in {'Enum', 'object'}:
                        properties[field_name]['type'] = python_type_2_json.get(type_.__name__, type_.__name__)
                properties[field_name]['enum'] = list(field.type_.__members__)
            else:
                properties[field_name]['type'] = python_type_2_json.get(field.type_.__name__, field.type_.__name__)

        schema = {
            'name': model_class.Meta.name,
            'description': model_class.Meta.description,
            'parameters': {
                'type': 'object',
                'properties': properties,
                'required': required,
            }
        }
        cls.__schema_cache__['function_calling_schema'] = schema
        return schema

    class Meta:
        name = ""  # 工具名称
        description = ""  # 工具描述


class ObservableMixin(ABC):

    def __init__(self):
        self.observer_list = []

    def add_handler(self, observer):
        self.observer_list.append(observer)

    def notify(self, *args, **kwargs):
        for observer in self.observer_list:
            observer.handle(*args, **kwargs)


class Observer(ABC):
    def handle(self, *args, **kwargs):
        raise NotImplementedError
