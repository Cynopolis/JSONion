import json
import argparse
from pathlib import Path


def generate(source_path: Path, build_dir: Path):
    with source_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    build_dir.mkdir(parents=True, exist_ok=True)
    output_file = build_dir / "commands.py"

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
            comment = field_comments[idx] if idx < len(field_comments) else ""
            if comment:
                lines.append(f"    # {comment}")
            lines.append(f"    {field_name}: {field_type}")

        lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Python @dataclass definitions from a command JSON file."
    )
    parser.add_argument(
        "-s", "--source",
        required=True,
        type=Path,
        help="Path to the source JSON file"
    )
    parser.add_argument(
        "-b", "--build",
        required=True,
        type=Path,
        help="Path to the build output directory"
    )

    args = parser.parse_args()
    generate(args.source, args.build)


if __name__ == "__main__":
    main()
