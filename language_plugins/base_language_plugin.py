from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseLanguagePlugin(ABC):
    """
    Abstract base class for language generators.
    """

    output_folder: str

    def generate(self, all_json_data: Dict[str, Dict[str, Any]], build_root: Path) -> None:
        """
        Orchestrates generation:
        - validates ABOUT sections
        - creates language subfolder
        - calls generate_code()
        - writes all output files
        """
        # Validate each JSON file
        for filename, data in all_json_data.items():
            self._validate_about_sections(data)

        output_dir = build_root / self.output_folder
        output_dir.mkdir(parents=True, exist_ok=True)

        # Plugin returns dict: {filename -> content}
        files_dict = self.generate_code(all_json_data)

        for filename, content in files_dict.items():
            file_path = output_dir / filename
            file_path.write_text(content, encoding="utf-8")

    @abstractmethod
    def generate_code(self, all_json_data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """
        Generate a dictionary of filename -> file content for this language.
        `all_json_data` is a dict of {source_filename: json_object}.
        """
        pass

    def _validate_about_sections(self, data: Dict[str, Any]) -> None:
        for command_name, command_body in data.items():
            fields = [k for k in command_body.keys() if k != "ABOUT"]
            about = command_body.get("ABOUT")

            if about is None:
                raise ValueError(
                    f"Command '{command_name}' is missing the ABOUT section.")

            expected_entries = 1 + len(fields)
            actual_entries = len(about)

            if actual_entries != expected_entries:
                raise ValueError(
                    f"Command '{command_name}' has an incomplete ABOUT section: "
                    f"expected {expected_entries} entries (1 class doc + {len(fields)} field(s)), "
                    f"but found {actual_entries}."
                )
