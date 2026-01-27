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
            about = command_body.get("ABOUT")
            if about is None:
                raise ValueError(
                    f"Command '{command_name}' is missing the ABOUT section.")

            # Validate each field
            for field_name, field_info in command_body.items():
                if field_name == "ABOUT":
                    continue
                if not isinstance(field_info, dict):
                    raise ValueError(
                        f"Field '{field_name}' in command '{command_name}' must be an object with 'type' and 'comment'."
                    )
                if "type" not in field_info:
                    raise ValueError(
                        f"Field '{field_name}' in command '{command_name}' is missing 'type'."
                    )
                if "comment" not in field_info:
                    raise ValueError(
                        f"Field '{field_name}' in command '{command_name}' is missing 'comment'."
                    )
