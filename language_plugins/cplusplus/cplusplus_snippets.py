from language_plugins.base_snippets import Snippets
from language_plugins.command_definitions import Command, CommandEntry, EntryType


class CppSnippet(Snippets):
    indent: str = "    "

    def get_file_snippet(self, commands: list[Command]) -> str:
        """
        Generate the full C++ header (.hpp) file.
        """
        header = self.get_header_snippet()
        lines = []

        for command in commands:
            lines.extend(self.get_command_snippet(command))

        command_str = super().snippet_to_str(lines, 1)

        for i, line in enumerate(header):
            try:
                header[i] = line.format(commands_key=command_str)
            except (ValueError, KeyError):
                pass

        return "\n".join(header)

    def get_command_snippet(self, command: Command) -> list[str]:
        """
        Generate documentation and class definition for one command.
        """
        lines = self.get_about_snippet(command)
        lines.extend(self.get_class_snippet(command))
        return lines

    def get_header_snippet(self) -> list[str]:
        """
        Generate top-of-file header.
        """
        return [
            "// Auto-generated file. Do not edit manually.",
            "#pragma once",
            "",
            "#include <string>",
            "#include <optional>",
            "",
            "namespace GeneratedCommands",
            "{",
            "{commands_key}",
            "}"
        ]

    def get_class_snippet(self, command: Command) -> list[str]:
        """
        Generate the C++ class definition.
        """
        lines = [
            f"class {command.name} : public Command",
            "{",
            "public:"
        ]

        lines.extend(
            super().indent_snippet(self.get_entries_snippet(command), 1)
        )

        lines.append("};\n")
        return lines

    def get_about_snippet(self, command: Command) -> list[str]:
        """
        Generate a block-style Doxygen comment for the class.
        """
        if not command.about:
            return []

        lines = [
            "/**",
            " * @brief " + command.about.splitlines()[0].strip()
        ]

        for line in command.about.splitlines()[1:]:
            lines.append(f" * {line.strip()}")

        lines.append(" */")
        return lines

    def get_entries_snippet(self, command: Command) -> list[str]:
        """
        Generate all member variable declarations.
        """
        if not command.entries:
            return ["// No fields defined"]

        lines = []
        for entry in command.entries:
            lines.extend(self.get_entry_snippet(entry))
        return lines

    def get_entry_snippet(self, entry: CommandEntry) -> list[str]:
        """
        Generate a single member variable with a block Doxygen comment.
        """
        cpp_name = entry.name
        lines = []

        cpp_type = {
            EntryType.STRING: "std::string",
            EntryType.INT: "int",
            EntryType.FLOAT: "float",
            EntryType.BOOL: "bool",
        }[entry.type]

        if entry.optional:
            cpp_type = f"std::optional<{cpp_type}>"

        if entry.comment:
            lines.extend([
                "/**",
                f" * @brief {entry.comment.strip()}",
                " */"
            ])

        lines.append(f"{cpp_type} {cpp_name};")
        return lines
