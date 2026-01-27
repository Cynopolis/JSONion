import re
from pathlib import Path
from typing import Dict, Any
from language_plugins.base_language_plugin import BaseLanguagePlugin


class PythonLanguagePlugin(BaseLanguagePlugin):
    output_folder = "python"

    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def generate_code(self, all_json_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """
        Generate a dictionary of filename -> file content.
        Each JSON source file becomes its own .py file.
        Also includes a copy of base_command.py.
        """
        output_files = {}

        # Include the base_command.py file by reading it from disk
        output_files["base_command.py"] = self._get_base_command_code()

        # Generate code per JSON source file
        for source_filename, data in all_json_data.items():
            output_files[f"{source_filename}.py"] = self._generate_file_code(
                data)

        return output_files

    def _generate_file_code(self, data: Dict[str, Any]) -> str:
        lines = [
            "from dataclasses import dataclass",
            "from typing import Optional",
            "from .base_command import Command",
            "",
            "# This file is auto-generated. Do not edit manually.",
            "",
        ]

        for command_name, command_body in data.items():
            about = command_body.get("ABOUT")
            fields_info = [(k, v)
                           for k, v in command_body.items() if k != "ABOUT"]

            lines.append("@dataclass")
            # inherit from Command
            lines.append(f"class {command_name}(Command):")
            lines.append('    """')

            # Handle ABOUT string or list properly
            if isinstance(about, str):
                about_lines = about.splitlines()
            elif isinstance(about, list):
                about_lines = about
            else:
                about_lines = [f"{command_name} command."]

            for line in about_lines:
                lines.append(f"    {line.strip()}")

            lines.append('    """')

            if not fields_info:
                lines.append("    pass")
                lines.append("")
                continue

            for field_name, field_info in fields_info:
                python_name = self.camel_to_snake(field_name)
                field_type = field_info["type"]
                comment = field_info.get("comment", "")

                if comment:
                    lines.append(f"    # {comment}")
                lines.append(f"    {python_name}: {field_type}")

            lines.append("")

        return "\n".join(lines)

    def _get_base_command_code(self) -> str:
        """Read the existing base_command.py file and return its contents as a string"""
        base_file = Path(__file__).parent / "base_command.py"
        if not base_file.exists():
            raise FileNotFoundError(
                f"Cannot find base_command.py at {base_file}")
        return base_file.read_text(encoding="utf-8")
