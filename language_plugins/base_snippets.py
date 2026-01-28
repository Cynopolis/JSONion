import re
from abc import ABC, abstractmethod
from .command_definitions import Command, CommandEntry


class Snippets(ABC):
    indent: str

    def indent_snippet(self, snippet: list[str], indents: int) -> list[str]:
        indented_snippet: list[str] = []
        indent_string = self.indent*indents
        for line in snippet:
            indented_snippet.append(indent_string + line)
        return indented_snippet

    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    @staticmethod
    def to_pascal_case(name: str) -> str:
        if "_" in name:
            return "".join(part.capitalize() for part in name.split("_"))
        return name[0].upper() + name[1:]

    def snippet_to_str(self, snippet: list[str], indents: int = 0) -> str:
        if indents == 0:
            return "\n".join(snippet)
        else:
            return "\n".join(self.indent_snippet(snippet, indents))

    @abstractmethod
    def get_file_snippet(self, commands: list[Command]) -> str:
        pass

    @abstractmethod
    def get_command_snippet(self, command: Command) -> list[str]:
        pass

    @abstractmethod
    def get_header_snippet(self) -> list[str]:
        pass

    @abstractmethod
    def get_class_snippet(self, command: Command) -> list[str]:
        pass

    @abstractmethod
    def get_about_snippet(self, command: Command) -> list[str]:
        pass

    @abstractmethod
    def get_entries_snippet(self, command: Command) -> list[str]:
        pass

    @abstractmethod
    def get_entry_snippet(self, command: Command) -> list[str]:
        pass
