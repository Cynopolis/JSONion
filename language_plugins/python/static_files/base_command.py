import json
import re
from dataclasses import asdict, fields, is_dataclass
from typing import Type, TypeVar, Any

T = TypeVar("T", bound="Command")


class Command:
    """
    Base class for all generated commands.
    Provides:
    - automatic JSON serialization/deserialization
    - a command_name field in snake_case matching the class name
    """

    command_name: str

    def __post_init__(self):
        # Set command_name automatically from the class name
        if not hasattr(self, "command_name") or self.command_name is None:
            self.command_name = self._class_name_to_snake()

    def _class_name_to_snake(self) -> str:
        name = self.__class__.__name__

        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def to_json(self) -> str:
        """
        Convert this command instance into a JSON string.
        """
        if not is_dataclass(self):
            raise TypeError(
                f"{self.__class__.__name__} must be a dataclass to use to_json()")
        return json.dumps(asdict(self), ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """
        Create an instance of the command from a JSON string.
        """
        if not is_dataclass(cls):
            raise TypeError(
                f"{cls.__name__} must be a dataclass to use from_json()")
        data = json.loads(json_str)
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)
