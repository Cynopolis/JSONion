from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseLanguagePlugin(ABC):
    """
    Abstract base class for language generators.
    """

    output_folder: str
    output_filename: str

    def generate(self, data: Dict[str, Any], build_root: Path) -> None:
        """
        Orchestrates generation:
        - creates language subfolder
        - calls generate_code()
        - writes output file
        """
        output_dir = build_root / self.output_folder
        output_dir.mkdir(parents=True, exist_ok=True)

        code = self.generate_code(data)

        output_file = output_dir / self.output_filename
        output_file.write_text(code, encoding="utf-8")

    @abstractmethod
    def generate_code(self, data: Dict[str, Any]) -> str:
        """
        Generate the source code text for this language.
        """
        pass
