import re
from pathlib import Path
from typing import Dict, List
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

        for source_filename, commands in all_json_data.items():
            output_files[f"{source_filename}.js"] = self._generate_file_code(
                commands)

        return output_files

    def _generate_file_code(self, commands: List[Command]) -> str:
        lines = [
            "// Auto-generated file. Do not edit manually.",
            "import { Command } from './BaseCommand.js';",
            "",
        ]

        exported_names: List[str] = []

        for command in commands:
            exported_names.append(command.name)

            # JSDoc for class
            if command.about:
                lines.append("/**")
                for line in command.about.splitlines():
                    lines.append(f" * {line.strip()}")
                lines.append(" */")

            lines.append(f"class {command.name} extends Command {{")
            lines.append("    constructor() {")
            lines.append("        super();")

            if not command.entries:
                lines.append("        // No fields defined")
            else:
                for entry in command.entries:
                    js_name = self.camel_to_snake(entry.name)

                    if entry.comment:
                        lines.append(f"        // {entry.comment}")

                    # Default value: null works well for optional & non-optional in JS
                    lines.append(f"        this.{js_name} = null;")

            lines.append("    }")
            lines.append("}")
            lines.append("")

        if exported_names:
            exports = ", ".join(exported_names)
            lines.append(f"export {{ {exports} }};")

        return "\n".join(lines)

    def _get_base_command_code(self) -> str:
        """Return the contents of BaseCommand.js"""
        base_file = Path(__file__).parent / "BaseCommand.js"
        if not base_file.exists():
            raise FileNotFoundError(
                f"Cannot find BaseCommand.js at {base_file}"
            )
        return base_file.read_text(encoding="utf-8")
