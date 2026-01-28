from pathlib import Path

from language_plugins.base_language_plugin import BaseLanguagePlugin
from language_plugins.base_snippets import Snippets
from .cplusplus_snippets import CPlusPlusSnippets


class CPlusPlusLanguagePlugin(BaseLanguagePlugin):
    output_folder = "cplusplus"
    file_ending = "hpp"
    static_file_path = Path(__file__).parent / "static_files"
    snippets: Snippets = CPlusPlusSnippets()
