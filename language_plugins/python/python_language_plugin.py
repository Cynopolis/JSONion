from pathlib import Path

from language_plugins.base_language_plugin import BaseLanguagePlugin
from language_plugins.base_snippets import Snippets
from .python_snippets import PythonSnippets


class PythonLanguagePlugin(BaseLanguagePlugin):
    output_folder = "python"
    file_ending = "py"
    static_file_path = Path(__file__).parent / "static_files"
    snippets: Snippets = PythonSnippets()
