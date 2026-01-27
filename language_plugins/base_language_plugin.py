from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseLanguagePlugin(ABC):
    """
    Abstract base class for language generators.
    """

    output_folder: str

    def generate(self, data: Dict[str, Any], build_root: Path) -> None:
        """
        Orchestrates generation:
        - creates language subfolder
        - calls generate_code()
        - writes all output files
        """
        output_dir = build_root / self.output_folder
        output_dir.mkdir(parents=True, exist_ok=True)

        files_dict = self.generate_code(data)  # now a dict of filename -> text

        for filename, content in files_dict.items():
            file_path = output_dir / filename
            file_path.write_text(content, encoding="utf-8")

    @abstractmethod
    def generate_code(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate a dictionary of filename -> file content for this language.
        """
        pass
