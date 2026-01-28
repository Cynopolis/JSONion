from language_plugins.base_snippets import Snippets
from language_plugins.command_definitions import Command, CommandEntry, EntryType


class JavascriptSnippets(Snippets):
    indent: str = "    "

    def get_file_snippet(self, commands: list[Command]) -> str:
        lines = self.get_header_snippet()
        for command in commands:
            lines.extend(self.get_command_snippet(command))
        lines.extend(self._get_footer_snippet(commands))
        return super().snippet_to_str(lines)

    def get_command_snippet(self, command: Command) -> list[str]:
        lines = self.get_about_snippet(command)
        lines.extend(self.get_class_snippet(command))

        return lines

    def get_header_snippet(self):
        lines = [
            "// Auto-generated file. Do not edit manually.",
            "import { Command } from './BaseCommand.js';",
            "",
        ]
        return lines

    def get_about_snippet(self, command: Command) -> list[str]:
        lines = []
        if command.about:
            lines.append("/**")
            for line in command.about.splitlines():
                lines.append(f" * {line.strip()}")
                lines.append(" */")
        return lines

    def get_class_snippet(self, command: Command) -> list[str]:
        lines = [
            f"class {command.name} extends Command {{",
        ]
        lines.extend(super().indent_snippet(
            self.get_entries_snippet(command), 1))
        lines.append("}\n")
        return lines

    def get_entries_snippet(self, command: Command) -> list[str]:
        lines = [
            "constructor() {",
            self.indent + "super();"
        ]
        if not command.entries:
            no_commands = [
                "// No fields defined"
            ]
            lines.extend(super().indent_snippet(no_commands, 1))
        else:
            for entry in command.entries:
                lines.extend(super().indent_snippet(
                    self.get_entry_snippet(entry), 1))

        lines.append("}")
        return lines

    def get_entry_snippet(self, entry: CommandEntry) -> list[str]:
        csharp_name = Snippets.camel_to_snake(entry.name)

        lines = []

        if entry.comment:
            lines.append(f"// {entry.comment}")

        lines.append(f"this.{csharp_name} = null;")
        return lines

    def _get_footer_snippet(self, commands: list[Command]) -> list[str]:
        command_names: list[str] = [command.name for command in commands]
        return [
            f"export {{ {", ".join(command_names)} }};"
        ]
