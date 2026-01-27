import re
from typing import Dict, Any
from language_plugins.base_language_plugin import BaseLanguagePlugin


class PythonLanguagePlugin(BaseLanguagePlugin):
    output_folder = "python"

    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def generate_code(self, all_json_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        output_files = {}
        for source_filename, data in all_json_data.items():
            output_files[f"{source_filename}.py"] = self._generate_file_code(
                data)
        return output_files

    def _generate_file_code(self, data: Dict[str, Any]) -> str:
        lines = [
            "from dataclasses import dataclass",
            "from typing import Optional",
            "",
            "# This file is auto-generated. Do not edit manually.",
            "",
        ]

        for command_name, command_body in data.items():
            about = command_body.get("ABOUT")
            fields = [(k, v) for k, v in command_body.items() if k != "ABOUT"]

            lines.append("@dataclass")

            lines.append(f"class {command_name}:")
            lines.append('    """')

            # Handle ABOUT string or list properly
            if isinstance(about, str):
                about_lines = about.splitlines()
            else:
                about_lines = about  # already a list

            for line in about_lines:
                lines.append(f"    {line.strip()}")

            lines.append('    """')

            if not fields:
                lines.append("    pass")
                lines.append("")
                continue

            for field_name, field_info in fields:
                python_name = self.camel_to_snake(field_name)
                field_type = field_info["type"]
                comment = field_info.get("comment", "")

                if comment:
                    lines.append(f"    # {comment}")
                lines.append(f"    {python_name}: {field_type}")

            lines.append("")

        return "\n".join(lines)
