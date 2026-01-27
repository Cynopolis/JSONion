import json
import argparse
from pathlib import Path

import language_plugins
from language_plugins.base_language_plugin import BaseLanguagePlugin


def load_plugins() -> dict[str, type[BaseLanguagePlugin]]:
    """
    Load all language plugins listed in language_plugins.__all__.
    Returns a dict mapping language name -> plugin class.
    """
    plugins = {}

    for plugin_name in language_plugins.__all__:
        plugin_cls = getattr(language_plugins, plugin_name)

        if not issubclass(plugin_cls, BaseLanguagePlugin):
            continue

        # PythonLanguagePlugin -> python
        language_key = plugin_name.replace("LanguagePlugin", "").lower()
        plugins[language_key] = plugin_cls

    return plugins


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
        help="Target language (default: generate all languages)"
    )

    args = parser.parse_args()

    with args.source.open("r", encoding="utf-8") as f:
        data = json.load(f)

    plugins = load_plugins()
    if not plugins:
        raise RuntimeError("No language plugins registered.")

    if args.language:
        lang = args.language.lower()
        if lang not in plugins:
            raise ValueError(
                f"Unsupported language '{args.language}'. "
                f"Available languages: {', '.join(sorted(plugins.keys()))}"
            )
        selected_plugins = {lang: plugins[lang]}
    else:
        selected_plugins = plugins  # generate all languages

    for lang, plugin_cls in selected_plugins.items():
        print(f"Generating {lang}...")
        plugin = plugin_cls()
        plugin.generate(data, args.build)
        print(f"{lang} generation complete.")


if __name__ == "__main__":
    main()
