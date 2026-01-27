import re
from typing import Dict, Any

from .base_language_plugin import BaseLanguagePlugin


class PythonLanguagePlugin(BaseLanguagePlugin):
    output_folder = "python"

    @staticmethod
    def camel_to_snake(name: str) -> str:
        """Convert CamelCase or CapitolCamelCase to snake_case"""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def generate_code(self, all_json_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """
        Generate Python code for all JSON files.
        Returns a dict mapping output filename -> file content.
        """
        output_files = {}

        for source_filename, data in all_json_data.items():
            output_files[f"{source_filename}.py"] = self._generate_file_code(
                data)

        return output_files

    def _generate_file_code(self, data: Dict[str, Any]) -> str:
        """
        Generate the Python code for a single JSON object (i.e., one file).
        """
        lines = [
            "from dataclasses import dataclass",
            "from typing import Optional",
            "",
            "# This file is auto-generated. Do not edit manually.",
            "",
        ]

        for command_name, command_body in data.items():
            about = command_body.get("ABOUT", [])
            fields = [(k, v) for k, v in command_body.items() if k != "ABOUT"]

            # Class docstring
            class_doc = about[0] if about else f"{command_name} command."
            lines.append("@dataclass")
            lines.append(f"class {command_name}:")
            lines.append("    \"\"\"")
            for line in class_doc.splitlines():
                lines.append(f"    {line}")
            lines.append("    \"\"\"")

            # Handle empty classes
            if not fields:
                lines.append("    pass")
                lines.append("")
                continue

            # Field comments start from index 1 in ABOUT
            field_comments = about[1:]

            for idx, (field_name, field_type) in enumerate(fields):
                python_name = self.camel_to_snake(field_name)
                comment = field_comments[idx] if idx < len(
                    field_comments) else ""

                if comment:
                    lines.append(f"    # {comment}")
                lines.append(f"    {python_name}: {field_type}")

            lines.append("")

        return "\n".join(lines)
