import json
import argparse
from pathlib import Path

import language_plugins
from language_plugins.base_language_plugin import BaseLanguagePlugin


def load_plugins() -> dict[str, type[BaseLanguagePlugin]]:
    plugins = {}
    for plugin_name in language_plugins.__all__:
        plugin_cls = getattr(language_plugins, plugin_name)
        if not issubclass(plugin_cls, BaseLanguagePlugin):
            continue
        language_key = plugin_name.replace("LanguagePlugin", "").lower()
        plugins[language_key] = plugin_cls
    return plugins


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate language-specific code from command JSON files.\n"
            "You can provide a single JSON file or a folder containing multiple JSON files.\n"
            "By default, code will be generated for all available languages unless -l is specified."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-s", "--source",
        required=True,
        type=Path,
        help="Path to the source JSON file or folder containing JSON files"
    )
    parser.add_argument(
        "-b", "--build",
        required=True,
        type=Path,
        help="Path to the build output directory"
    )
    parser.add_argument(
        "-l", "--language",
        help=(
            "Target language to generate (e.g., python, csharp).\n"
            "Default: generate all available languages"
        )
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Code Generator 1.0",
        help="Show the generator version and exit"
    )

    args = parser.parse_args()

    # Gather JSON files
    json_files = {}
    if args.source.is_file() and args.source.suffix.lower() == ".json":
        json_files[args.source.stem] = args.source
    elif args.source.is_dir():
        for file_path in args.source.glob("*.json"):
            json_files[file_path.stem] = file_path
        if not json_files:
            raise ValueError(f"No JSON files found in folder '{args.source}'.")
    else:
        raise ValueError(
            f"Source must be a JSON file or folder, got '{args.source}'.")

    # Load JSON content into dict
    all_json_data = {}
    for filename, path in json_files.items():
        with path.open("r", encoding="utf-8") as f:
            all_json_data[filename] = json.load(f)

    plugins = load_plugins()
    if not plugins:
        raise RuntimeError("No language plugins registered.")

    if args.language:
        lang_key = args.language.lower()
        if lang_key not in plugins:
            raise ValueError(f"Unsupported language '{args.language}'.")
        selected_plugins = {lang_key: plugins[lang_key]}
    else:
        selected_plugins = plugins

    # Pass the dict of all JSON files to each plugin
    for lang, plugin_cls in selected_plugins.items():
        print(f"Generating {lang}...")
        plugin = plugin_cls()
        plugin.generate(all_json_data, args.build)
        print(f"{lang} generation complete.")


if __name__ == "__main__":
    main()
