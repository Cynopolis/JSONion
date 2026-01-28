from language_plugins.base_snippets import Snippets
from language_plugins.command_definitions import Command, CommandEntry, EntryType


class PythonSnippets(Snippets):
    indent: str = "    "

    def get_file_snippet(self, commands: list[Command]) -> str:
        lines = self.get_header_snippet()
        for command in commands:
            lines.extend(self.get_command_snippet(command))

        return "\n".join(lines)

    def get_command_snippet(self, command: Command) -> list[str]:
        lines = self.get_class_snippet(command.name)
        lines.extend(super().indent_snippet(
            self.get_about_snippet(command.about), 1))
        lines.extend(super().indent_snippet(
            self.get_entries_snippet(command.entries), 1))
        lines.append("\n")
        return lines

    def get_header_snippet(self):
        lines = [
            "from dataclasses import dataclass",
            "from typing import Optional",
            "from .base_command import Command",
            "",
            "# This file is auto-generated. Do not edit manually.",
            "",
        ]
        return lines

    def get_class_snippet(self, command_name: str) -> list[str]:
        lines = []
        lines.append("@dataclass")
        lines.append(f"class {command_name}(Command):")

        return lines

    def get_about_snippet(self, about: str) -> list[str]:
        lines = []
        lines.append('"""')

        for line in about.splitlines():
            lines.append(f"{line.strip()}")

        lines.append('"""')
        return lines

    def get_entries_snippet(self, entries: list[CommandEntry]) -> list[str]:
        if not entries:
            return ["pass"]

        lines = []
        for entry in entries:
            lines.extend(self.get_entry_snippet(entry))
        return lines

    def get_entry_snippet(self, entry: CommandEntry) -> list[str]:
        python_name = self.camel_to_snake(entry.name)

        lines = []

        py_type = {
            EntryType.STRING: "str",
            EntryType.INT: "int",
            EntryType.FLOAT: "float",
            EntryType.BOOL: "bool",
        }[entry.type]

        if entry.optional:
            py_type = f"Optional[{py_type}]"

        if entry.comment:
            lines.append(f"# {entry.comment}")

        lines.append(f"{python_name}: {py_type}")
        return lines
