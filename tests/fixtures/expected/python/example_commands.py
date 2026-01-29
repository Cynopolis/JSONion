from dataclasses import dataclass
from typing import Optional
from .base_command import Command

# This file is auto-generated. Do not edit manually.

@dataclass
class ExampleCommand(Command):
    """
    This is a test command.
    """
    # Example message
    some_message: str
    # Example count
    count: int
    # Example bool
    some_boolean_example: bool
    # Optional string
    could_be_nothing: Optional[str]


@dataclass
class AnotherExampleCommand(Command):
    """
    This command just shows another example.
    """
    pass

