from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseLanguagePlugin(ABC):
    """
    Abstract base class for language generators.
    """

    # output subfolder to contain the autogenerate code for a specific language
    output_folder: str

    @abstractmethod
    def generate(self, data: Dict[str, Any], output_dir: Path) -> None:
        """
        Generate language-specific output.

        :param data: Parsed JSON dictionary
        :param output_dir: Language-specific output directory
        """
        pass
