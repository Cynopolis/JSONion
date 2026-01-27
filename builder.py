import json
import argparse
from pathlib import Path

from language_plugins.python_language_plugin import PythonLanguagePlugin


def main():
    parser = argparse.ArgumentParser(
        description="Generate language-specific code from a command JSON file."
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
    parser.add_argument(
        "-l", "--language",
        default="python",
        help="Target language (default: python)"
    )

    args = parser.parse_args()

    with args.source.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if args.language == "python":
        plugin = PythonLanguagePlugin()
    else:
        raise ValueError(f"Unsupported language: {args.language}")

    language_output_dir = args.build / plugin.output_folder
    plugin.generate(data, language_output_dir)


if __name__ == "__main__":
    main()
