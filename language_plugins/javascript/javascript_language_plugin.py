import re
from pathlib import Path
from typing import Dict, List
from .javascript_snippets import JavascriptSnippets
from language_plugins.base_language_plugin import BaseLanguagePlugin
from language_plugins.command_definitions import Command, CommandEntry


class JavaScriptLanguagePlugin(BaseLanguagePlugin):
    output_folder = "javascript"

    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def generate_code(self, all_json_data: Dict[str, List[Command]]) -> Dict[str, str]:
        output_files: Dict[str, str] = {}

        # Include BaseCommand.js
        output_files["BaseCommand.js"] = self._get_base_command_code()

        snippets = JavascriptSnippets()
        for source_filename, commands in all_json_data.items():
            output_files[f"{source_filename}.js"] = snippets.get_file_snippet(
                commands)

        return output_files

    def _get_base_command_code(self) -> str:
        """Return the contents of BaseCommand.js"""
        base_file = Path(__file__).parent / "BaseCommand.js"
        if not base_file.exists():
            raise FileNotFoundError(
                f"Cannot find BaseCommand.js at {base_file}"
            )
        return base_file.read_text(encoding="utf-8")
