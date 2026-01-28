from language_plugins.base_snippets import Snippets
from language_plugins.command_definitions import Command, CommandEntry, EntryType


class CSharpSnippet(Snippets):
    indent: str = "    "

    def get_file_snippet(self, commands: list[Command]) -> str:
        header = self.get_header_snippet()
        lines = []
        for command in commands:
            lines.extend(self.get_command_snippet(command))
        command_str = super().snippet_to_str(lines, 1)
        for i, line in enumerate(header):
            try:
                header[i] = line.format(commands_key=command_str)
            except ValueError:
                pass
            except KeyError as e:
                print(e)

        return "\n".join(header)

    def get_command_snippet(self, command: Command) -> list[str]:
        lines = self.get_about_snippet(command)
        lines.extend(self.get_class_snippet(command))

        return lines

    def get_header_snippet(self):
        lines = [
            "// Auto-generated file. Do not edit manually.",
            "using System;",
            "",
            "namespace GeneratedCommands",
            "{",
            "{commands_key}",
            "}"
        ]
        return lines

    def get_class_snippet(self, command: Command) -> list[str]:
        lines = [
            f"public class {command.name} : Command",
            "{"
        ]
        lines.extend(super().indent_snippet(
            self.get_entries_snippet(command), 1))
        lines.append("}\n")
        return lines

    def get_about_snippet(self, command: Command) -> list[str]:
        lines = []
        if command.about:
            lines.append("/// <summary>")
            for line in command.about.splitlines():
                lines.append(f"/// {line.strip()}")
                lines.append("/// </summary>")
        return lines

    def get_entries_snippet(self, command: Command) -> list[str]:
        if not command.entries:
            return ["// No fields defined"]

        lines = []
        for entry in command.entries:
            lines.extend(self.get_entry_snippet(entry))
        return lines

    def get_entry_snippet(self, entry: CommandEntry) -> list[str]:
        csharp_name = Snippets.to_pascal_case(entry.name)

        lines = []

        csharp_type = {
            EntryType.STRING: "string",
            EntryType.INT: "int",
            EntryType.FLOAT: "float",
            EntryType.BOOL: "bool",
        }[entry.type]

        if entry.optional:
            csharp_type = f"{csharp_type}?"

        if entry.comment:
            lines.append(f"// {entry.comment}")

        lines.append(f"public {csharp_type} {csharp_name} {{ get; set; }}")
        return lines
