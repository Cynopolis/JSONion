from typing import Dict, List
from pathlib import Path
from .csharp_snippets import CSharpSnippet
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
        snippets = CSharpSnippet()
        for source_filename, commands in all_json_data.items():
            output_files[f"{source_filename}.cs"] = snippets.get_file_snippet(
                commands)

        return output_files

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
