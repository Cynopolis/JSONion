from pathlib import Path
from typing import Dict, Any
import shutil

from .base_snippets import Snippets
from .command_definitions import Command, CommandEntry, EntryType


class BaseLanguagePlugin:
    """
    Abstract base class for language generators.
    """
    output_folder: str
    file_ending: str
    static_file_path: str
    snippets: Snippets

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

        # parse the json files into a list of commands
        parsed_json_data: Dict[str, list[Command]] = {}
        for file_name, json_contents in all_json_data.items():
            parsed_json_data[file_name] = self._convert_json_to_commands(
                json_contents)

        # Plugin returns dict: {filename -> content}
        files_dict = self._generate_code(parsed_json_data)

        for filename, content in files_dict.items():
            file_path = output_dir / filename
            file_path.write_text(content, encoding="utf-8")

        self._copy_static_files(self.static_file_path, output_dir)

    def _generate_code(self, all_json_data: Dict[str, list[Command]]) -> Dict[str, str]:
        """
        Generate a dictionary of filename -> file content for this language.
        `all_json_data` is a dict of {source_filename: json_object}.
        """
        output_files = {}

        # Generate code per JSON source file
        for source_filename, commands in all_json_data.items():
            output_files[f"{source_filename}.{self.file_ending}"] = self.snippets.get_file_snippet(
                commands)

        return output_files

    def _copy_static_files(self, static_file_dir: str, output_dir: str) -> None:
        src = Path(static_file_dir)
        dst = Path(output_dir)

        if not src.exists():
            raise FileNotFoundError(
                f"Static file directory does not exist: {src}")

        if not src.is_dir():
            raise NotADirectoryError(
                f"Static file path is not a directory: {src}")

        dst.mkdir(parents=True, exist_ok=True)

        for item in src.iterdir():
            target = dst / item.name

            if item.is_dir():
                # Copy directory tree (merge into existing directory)
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                # Copy file, overwrite if it exists
                shutil.copy2(item, target)

    def _convert_json_to_commands(self, single_json_file: Dict[str, Any]) -> list[Command]:
        parsed_commands: list[Command] = []

        for command_name, command_body in single_json_file.items():
            about: str = command_body["ABOUT"]
            entries: list[CommandEntry] = []

            for field_name, field_info in command_body.items():
                if field_name == "ABOUT":
                    continue

                type_str: str = field_info["type"]
                comment: str = field_info["comment"]
                optional: bool = field_info.get("optional", False)

                try:
                    entry_type = EntryType(type_str)
                except ValueError:
                    raise ValueError(
                        f"Unknown type '{type_str}' in command '{command_name}', field '{field_name}'."
                    )

                entries.append(
                    CommandEntry(
                        name=field_name,
                        type=entry_type,
                        comment=comment,
                        optional=optional,
                    )
                )

            parsed_commands.append(
                Command(
                    name=command_name,
                    about=about,
                    entries=entries,
                )
            )

        return parsed_commands

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
