import re
from typing import Dict, Any

from .base_language_plugin import BaseLanguagePlugin


class PythonLanguagePlugin(BaseLanguagePlugin):
    output_folder = "python"

    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def generate_code(self, data: Dict[str, Any]) -> Dict[str, str]:
        lines = []
        lines.append("from dataclasses import dataclass")
        lines.append("from typing import Optional")
        lines.append("")
        lines.append("# This file is auto-generated. Do not edit manually.")
        lines.append("")

        for command_name, command_body in data.items():
            about = command_body.get("ABOUT", [])
            fields = [(k, v) for k, v in command_body.items() if k != "ABOUT"]

            class_doc = about[0] if about else f"{command_name} command."

            lines.append("@dataclass")
            lines.append(f"class {command_name}:")
            lines.append("    \"\"\"")
            for line in class_doc.splitlines():
                lines.append(f"    {line}")
            lines.append("    \"\"\"")

            if not fields:
                lines.append("    pass")
                lines.append("")
                continue

            field_comments = about[1:]

            for idx, (field_name, field_type) in enumerate(fields):
                python_name = self.camel_to_snake(field_name)
                comment = field_comments[idx] if idx < len(
                    field_comments) else ""

                if comment:
                    lines.append(f"    # {comment}")
                lines.append(f"    {python_name}: {field_type}")

            lines.append("")

        return {"commands.py": "\n".join(lines)}
