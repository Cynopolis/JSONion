from pathlib import Path

from language_plugins.base_language_plugin import BaseLanguagePlugin
from language_plugins.base_snippets import Snippets
from .csharp_snippets import CSharpSnippet


class CSharpLanguagePlugin(BaseLanguagePlugin):
    output_folder = "csharp"
    file_ending = ".cs"
    static_file_path = Path(__file__).parent / "static_files"
    snippets: Snippets = CSharpSnippet()
