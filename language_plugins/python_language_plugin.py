import re
from pathlib import Path
from typing import Dict, Any
from .base_language_plugin import BaseLanguagePlugin


class PythonLanguagePlugin(BaseLanguagePlugin):
    output_folder = "python"
    OUTPUT_FILENAME = "commands.py"

    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def generate(self, data: Dict[str, Any], build_dir: Path) -> None:
        build_dir.mkdir(parents=True, exist_ok=True)
        output_file = build_dir / self.OUTPUT_FILENAME

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
            lines.append(f'    """{class_doc}"""')

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

        output_file.write_text("\n".join(lines), encoding="utf-8")
