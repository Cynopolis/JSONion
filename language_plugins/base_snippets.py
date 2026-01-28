import re
from abc import ABC, abstractmethod
from .command_definitions import Command, CommandEntry


class Snippets(ABC):
    indent: str

    def indent_snippet(self, snippet: list[str]) -> list[str]:
        indented_snippet: list[str] = []
        for line in snippet:
            indented_snippet.append(self.indent + line)
        return indented_snippet

    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

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
    def get_about_snippet(self, about: str) -> list[str]:
        pass

    @abstractmethod
    def get_no_entries_snippet(self, entries: list[CommandEntry]) -> list[str]:
        pass

    @abstractmethod
    def get_entry_snippet(self, entry: CommandEntry) -> list[str]:
        pass
