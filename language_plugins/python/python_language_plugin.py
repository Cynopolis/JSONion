import re
from pathlib import Path
from typing import Dict, Any
from language_plugins.base_language_plugin import BaseLanguagePlugin
from language_plugins.command_definitions import Command, CommandEntry, EntryType
from .python_snippets import PythonSnippets


class PythonLanguagePlugin(BaseLanguagePlugin):
    output_folder = "python"

    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def generate_code(self, all_json_data: Dict[str, list[Command]]) -> Dict[str, str]:
        """
        Generate a dictionary of filename -> file content.
        Each JSON source file becomes its own .py file.
        Also includes a copy of base_command.py.
        """
        output_files = {}

        # Include the base_command.py file by reading it from disk
        output_files["base_command.py"] = self._get_base_command_code()

        snippets = PythonSnippets()
        # Generate code per JSON source file
        for source_filename, commands in all_json_data.items():
            output_files[f"{source_filename}.py"] = snippets.get_file_snippet(
                commands)

        return output_files

    def _get_base_command_code(self) -> str:
        """Read the existing base_command.py file and return its contents as a string"""
        base_file = Path(__file__).parent / "base_command.py"
        if not base_file.exists():
            raise FileNotFoundError(
                f"Cannot find base_command.py at {base_file}")
        return base_file.read_text(encoding="utf-8")
