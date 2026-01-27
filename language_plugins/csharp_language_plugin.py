from typing import Dict, Any
from .base_language_plugin import BaseLanguagePlugin


class CSharpLanguagePlugin(BaseLanguagePlugin):
    output_folder = "csharp"

    def generate_code(self, all_json_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """
        Generate C# code for all JSON files.
        Returns a dict mapping output filename -> file content.
        """
        output_files = {}

        for source_filename, data in all_json_data.items():
            output_files[f"{source_filename}.cs"] = self._generate_file_code(
                data)

        return output_files

    def _generate_file_code(self, data: Dict[str, Any]) -> str:
        """
        Generate the C# code for a single JSON object (i.e., one file)
        """
        lines = [
            "// Auto-generated file. Do not edit manually.",
            "using System;",
            "",
            "namespace GeneratedCommands",
            "{",
        ]

        for command_name, command_body in data.items():
            about = command_body.get("ABOUT", [])
            fields = [(k, v) for k, v in command_body.items() if k != "ABOUT"]

            # Class documentation
            if about:
                lines.append("    /// <summary>")
                for line in about[0].splitlines():
                    lines.append(f"    /// {line}")
                lines.append("    /// </summary>")

            lines.append(f"    public class {command_name}")
            lines.append("    {")

            # Handle fields
            field_comments = about[1:] if about else []

            for idx, (field_name, field_type) in enumerate(fields):
                comment = field_comments[idx] if idx < len(
                    field_comments) else ""
                prop_name = self.to_pascal_case(field_name)
                cs_type = self.map_type(field_type)

                if comment:
                    lines.append(f"        // {comment}")
                lines.append(
                    f"        public {cs_type} {prop_name} {{ get; set; }}")

            # If no fields, insert a default constructor or leave empty class
            if not fields:
                lines.append("        // No fields defined")
            lines.append("    }")
            lines.append("")

        lines.append("}")  # namespace close
        return "\n".join(lines)

    @staticmethod
    def to_pascal_case(name: str) -> str:
        """
        Convert JSON field names (CamelCase or snake_case) to PascalCase
        """
        if "_" in name:
            parts = name.split("_")
            return "".join(part.capitalize() for part in parts)
        else:
            return name[0].upper() + name[1:]

    @staticmethod
    def map_type(json_type: str) -> str:
        """
        Map simplified JSON type strings to C# types
        """
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
            return json_type  # fallback
