from pathlib import Path

from language_plugins.base_language_plugin import BaseLanguagePlugin
from language_plugins.base_snippets import Snippets
from .javascript_snippets import JavascriptSnippets


class JavaScriptLanguagePlugin(BaseLanguagePlugin):
    output_folder = "javascript"
    file_ending = ".js"
    static_file_path = Path(__file__).parent / "static_files"
    snippets: Snippets = JavascriptSnippets()
