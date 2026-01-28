from enum import Enum
from dataclasses import dataclass


class EntryType(Enum):
    STRING = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"


@dataclass
class CommandEntry:
    name: str
    type: EntryType
    comment: str
    optional: bool = False


@dataclass
class Command:
    name: str
    about: str
    entries: list[CommandEntry]
