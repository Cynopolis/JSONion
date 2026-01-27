from typing import Dict, Any
from .base_language_plugin import BaseLanguagePlugin


class CSharpLanguagePlugin(BaseLanguagePlugin):
    output_folder = "csharp"

    def generate_code(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate C# class files from the JSON data.
        All commands are put into a single file 'Commands.cs' for simplicity.
        """
        lines = []
        lines.append("// Auto-generated file. Do not edit manually.")
        lines.append("using System;")
        lines.append("")
        lines.append("namespace GeneratedCommands")
        lines.append("{")

        for command_name, command_body in data.items():
            about = command_body.get("ABOUT", [])
            fields = [(k, v) for k, v in command_body.items() if k != "ABOUT"]

            # Class documentation
            if about:
                lines.append("    /// <summary>")
                lines.append(f"    /// {about[0]}")
                lines.append("    /// </summary>")

            lines.append(f"    public class {command_name}")
            lines.append("    {")

            for idx, (field_name, field_type) in enumerate(fields):
                comment = about[idx + 1] if idx + 1 < len(about) else ""
                prop_name = self.to_pascal_case(field_name)

                # Convert type hints to C# types
                cs_type = self.map_type(field_type)

                if comment:
                    lines.append(f"        // {comment}")
                lines.append(
                    f"        public {cs_type} {prop_name} {{ get; set; }}")

            lines.append("    }")
            lines.append("")

        lines.append("}")  # namespace close

        return {"Commands.cs": "\n".join(lines)}

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
            # For strings, use nullable reference type
            if inner == "str":
                return "string?"
            elif inner == "int":
                return "int?"
            elif inner == "bool":
                return "bool?"
            else:
                return f"{inner}?"  # fallback
        else:
            return json_type  # fallback, use as-is
