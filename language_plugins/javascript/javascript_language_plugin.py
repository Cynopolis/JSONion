import re
from pathlib import Path
from typing import Dict, Any
from language_plugins.base_language_plugin import BaseLanguagePlugin


class JavaScriptLanguagePlugin(BaseLanguagePlugin):
    output_folder = "javascript"

    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def generate_code(self, all_json_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        output_files = {}

        # Include BaseCommand.js
        output_files["BaseCommand.js"] = self._get_base_command_code()

        for source_filename, data in all_json_data.items():
            output_files[f"{source_filename}.js"] = self._generate_file_code(
                data)

        return output_files

    def _generate_file_code(self, data: Dict[str, Any]) -> str:
        lines = [
            "// Auto-generated file. Do not edit manually.",
            "import { Command } from './BaseCommand.js';",
            ""
        ]

        for command_name, command_body in data.items():
            about = command_body.get("ABOUT")
            fields = [(k, v) for k, v in command_body.items() if k != "ABOUT"]

            # Class doc
            if about:
                lines.append("/**")
                if isinstance(about, str):
                    about_lines = about.splitlines()
                else:
                    about_lines = about
                for line in about_lines:
                    lines.append(f" * {line.strip()}")
                lines.append(" */")

            # Class definition
            lines.append(f"class {command_name} extends Command " + "{")
            lines.append("    constructor() {")
            lines.append("        super();")

            for field_name, field_info in fields:
                js_name = self.camel_to_snake(field_name)
                comment = field_info.get("comment", "")
                default_value = "null"  # optional, could enhance later
                if comment:
                    lines.append(f"        // {comment}")
                lines.append(f"        this.{js_name} = {default_value};")
            lines.append("    }")
            lines.append("}")
            lines.append("")

        # Export all commands
        exports = ", ".join(data.keys())
        lines.append(f"export {{ {exports} }};")

        return "\n".join(lines)

    def _get_base_command_code(self) -> str:
        """Return the contents of BaseCommand.js"""
        base_file = Path(__file__).parent / "BaseCommand.js"
        if not base_file.exists():
            raise FileNotFoundError(
                f"Cannot find BaseCommand.js at {base_file}")
        return base_file.read_text(encoding="utf-8")
