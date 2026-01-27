from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseLanguagePlugin(ABC):
    """
    Abstract base class for language generators.
    """

    @abstractmethod
    def generate(self, data: Dict[str, Any], build_dir: Path) -> None:
        """
        Generate language-specific output from parsed JSON data.

        :param data: Parsed JSON dictionary
        :param build_dir: Output directory
        """
        pass
