import re
from abc import ABC, abstractmethod
from .command_definitions import Command, CommandEntry


class Snippets(ABC):
    """
    Abstract base class for generating code snippets for a given language.
    Provides utilities for indentation, casing conversions, and string formatting.
    Language-specific subclasses must implement the abstract methods to define
    how commands are rendered.
    """

    indent: str

    def indent_snippet(self, snippet: list[str], indents: int) -> list[str]:
        """
        Add indentation to each line in a snippet.

        Args:
            snippet (list[str]): List of lines to indent.
            indents (int): Number of indentation levels to apply.

        Returns:
            list[str]: New list of lines with indentation applied.
        """
        indented_snippet: list[str] = []
        indent_string = self.indent * indents
        for line in snippet:
            indented_snippet.append(indent_string + line)
        return indented_snippet

    @staticmethod
    def camel_to_snake(name: str) -> str:
        """
        Convert a camelCase or PascalCase string to snake_case.

        Args:
            name (str): The name to convert.

        Returns:
            str: The converted snake_case string.
        """
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    @staticmethod
    def to_pascal_case(name: str) -> str:
        """
        Convert a snake_case string to PascalCase.

        Args:
            name (str): The name to convert.

        Returns:
            str: The converted PascalCase string.
        """
        if "_" in name:
            return "".join(part.capitalize() for part in name.split("_"))
        return name[0].upper() + name[1:]

    def snippet_to_str(self, snippet: list[str], indents: int = 0) -> str:
        """
        Convert a list of lines into a single string, optionally indenting them.

        Args:
            snippet (list[str]): Lines of code or snippet.
            indents (int): Number of indentation levels to apply.

        Returns:
            str: Snippet as a single string with newlines and indentation.
        """
        if indents == 0:
            return "\n".join(snippet)
        else:
            return "\n".join(self.indent_snippet(snippet, indents))

    @abstractmethod
    def get_file_snippet(self, commands: list[Command]) -> str:
        """
        Generate the full contents of a source file for the given commands.

        Args:
            commands (list[Command]): List of Command objects to render.

        Returns:
            str: Full file content as a string.
        """
        pass

    @abstractmethod
    def get_command_snippet(self, command: Command) -> list[str]:
        """
        Generate the snippet for a single command, including its documentation
        and class definition.

        Args:
            command (Command): The Command object to render.

        Returns:
            list[str]: List of lines representing the command snippet.
        """
        pass

    @abstractmethod
    def get_header_snippet(self) -> list[str]:
        """
        Generate the top-of-file snippet, such as file comments, imports, or
        namespace declarations.

        Returns:
            list[str]: List of lines representing the file header.
        """
        pass

    @abstractmethod
    def get_about_snippet(self, command: Command) -> list[str]:
        """
        Generate the snippet for the 'ABOUT' section of a command, usually as
        documentation comments.

        Args:
            command (Command): The Command object.

        Returns:
            list[str]: Lines representing the ABOUT documentation.
        """
        pass

    @abstractmethod
    def get_class_snippet(self, command: Command) -> list[str]:
        """
        Generate the class definition snippet for a command, including braces
        and any nested entries.

        Args:
            command (Command): The Command object.

        Returns:
            list[str]: Lines representing the class definition.
        """
        pass

    @abstractmethod
    def get_entries_snippet(self, command: Command) -> list[str]:
        """
        Generate the snippet for all fields or entries of a command.

        Args:
            command (Command): The Command object.

        Returns:
            list[str]: Lines representing all fields of the command.
        """
        pass

    @abstractmethod
    def get_entry_snippet(self, command: Command) -> list[str]:
        """
        Generate the snippet for a single field or entry of a command, including
        type declaration and comment.

        Args:
            command (Command): The CommandEntry object.

        Returns:
            list[str]: Lines representing a single entry.
        """
        pass
