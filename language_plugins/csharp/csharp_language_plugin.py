from typing import Dict, List
from pathlib import Path
from language_plugins.base_language_plugin import BaseLanguagePlugin
from language_plugins.command_definitions import Command, CommandEntry, EntryType


class CSharpLanguagePlugin(BaseLanguagePlugin):
    output_folder = "csharp"

    def generate_code(self, all_json_data: Dict[str, List[Command]]) -> Dict[str, str]:
        """
        Generate a dict of filename -> file content for all JSON files.
        Includes a copy of BaseCommand.cs.
        """
        output_files: Dict[str, str] = {}

        # Include BaseCommand.cs
        output_files["BaseCommand.cs"] = self._get_base_command_code()

        for source_filename, commands in all_json_data.items():
            output_files[f"{source_filename}.cs"] = self._generate_file_code(
                commands)

        return output_files

    def _generate_file_code(self, commands: List[Command]) -> str:
        lines = [
            "// Auto-generated file. Do not edit manually.",
            "using System;",
            "",
            "namespace GeneratedCommands",
            "{",
        ]

        for command in commands:
            # XML doc comment
            if command.about:
                lines.append("    /// <summary>")
                for line in command.about.splitlines():
                    lines.append(f"    /// {line.strip()}")
                lines.append("    /// </summary>")

            lines.append(f"    public class {command.name} : Command")
            lines.append("    {")

            if not command.entries:
                lines.append("        // No fields defined")
            else:
                for entry in command.entries:
                    prop_name = self.to_pascal_case(entry.name)
                    cs_type = self.map_type(entry)

                    if entry.comment:
                        lines.append(f"        // {entry.comment}")

                    lines.append(
                        f"        public {cs_type} {prop_name} {{ get; set; }}"
                    )

            lines.append("    }")
            lines.append("")

        lines.append("}")  # namespace close
        return "\n".join(lines)

    def _get_base_command_code(self) -> str:
        """Read the BaseCommand.cs file from the C# plugin folder and return its contents"""
        base_file = Path(__file__).parent / "BaseCommand.cs"
        if not base_file.exists():
            raise FileNotFoundError(
                f"Cannot find BaseCommand.cs at {base_file}"
            )
        return base_file.read_text(encoding="utf-8")

    @staticmethod
    def to_pascal_case(name: str) -> str:
        if "_" in name:
            return "".join(part.capitalize() for part in name.split("_"))
        return name[0].upper() + name[1:]

    @staticmethod
    def map_type(entry: CommandEntry) -> str:
        base_type = {
            EntryType.STRING: "string",
            EntryType.INT: "int",
            EntryType.FLOAT: "float",
            EntryType.BOOL: "bool",
        }[entry.type]

        # Nullable reference / value types
        if entry.optional:
            return f"{base_type}?"

        return base_type
