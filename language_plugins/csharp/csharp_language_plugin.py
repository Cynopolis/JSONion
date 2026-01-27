from typing import Dict, Any
from pathlib import Path
from language_plugins.base_language_plugin import BaseLanguagePlugin


class CSharpLanguagePlugin(BaseLanguagePlugin):
    output_folder = "csharp"

    def generate_code(self, all_json_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """
        Generate a dict of filename -> file content for all JSON files.
        Includes a copy of BaseCommand.cs.
        """
        output_files = {}

        # Include BaseCommand.cs by reading it from the plugin folder
        output_files["BaseCommand.cs"] = self._get_base_command_code()

        # Generate each source file
        for source_filename, data in all_json_data.items():
            output_files[f"{source_filename}.cs"] = self._generate_file_code(
                data)

        return output_files

    def _generate_file_code(self, data: Dict[str, Any]) -> str:
        lines = [
            "// Auto-generated file. Do not edit manually.",
            "using System;",
            "using System.Text.Json;",
            "using System.Text.Json.Serialization;",
            "using System.Text.RegularExpressions;",
            "",
            "namespace GeneratedCommands",
            "{",
        ]

        for command_name, command_body in data.items():
            about = command_body.get("ABOUT")
            fields = [(k, v) for k, v in command_body.items() if k != "ABOUT"]

            # Class doc
            if about:
                lines.append("    /// <summary>")
                if isinstance(about, str):
                    about_lines = about.splitlines()
                else:
                    about_lines = about
                for line in about_lines:
                    lines.append(f"    /// {line.strip()}")
                lines.append("    /// </summary>")

            # Inherit from Command
            lines.append(f"    public class {command_name} : Command")
            lines.append("    {")

            if not fields:
                lines.append("        // No fields defined")
            else:
                for field_name, field_info in fields:
                    comment = field_info.get("comment", "")
                    prop_name = self.to_pascal_case(field_name)
                    cs_type = self.map_type(field_info["type"])

                    if comment:
                        lines.append(f"        // {comment}")
                    lines.append(
                        f"        public {cs_type} {prop_name} {{ get; set; }}")

            lines.append("    }")
            lines.append("")

        lines.append("}")  # namespace close
        return "\n".join(lines)

    def _get_base_command_code(self) -> str:
        """Read the BaseCommand.cs file from the C# plugin folder and return its contents"""
        base_file = Path(__file__).parent / "BaseCommand.cs"
        if not base_file.exists():
            raise FileNotFoundError(
                f"Cannot find BaseCommand.cs at {base_file}")
        return base_file.read_text(encoding="utf-8")

    @staticmethod
    def to_pascal_case(name: str) -> str:
        if "_" in name:
            parts = name.split("_")
            return "".join(part.capitalize() for part in parts)
        else:
            return name[0].upper() + name[1:]

    @staticmethod
    def map_type(json_type: str) -> str:
        if json_type == "str":
            return "string"
        elif json_type == "int":
            return "int"
        elif json_type == "bool":
            return "bool"
        elif json_type.startswith("Optional["):
            inner = json_type[len("Optional["):-1]
            if inner == "str":
                return "string?"
            elif inner == "int":
                return "int?"
            elif inner == "bool":
                return "bool?"
            else:
                return f"{inner}?"
        else:
            return json_type
