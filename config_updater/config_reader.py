"""Tweaked version of ConfigParser that supports case-sensitive keys."""

from configparser import ConfigParser
from dataclasses import dataclass
from typing import Self
from typing import Sequence
from typing import TextIO


class CaseSensitiveConfigParser(ConfigParser):
    def optionxform(self, option_str: str) -> str:
        return option_str


def load_config(file: TextIO, delimiters: Sequence[str] = ("=",)) -> ConfigParser:
    """Load config from the `file`."""
    config = CaseSensitiveConfigParser(delimiters=delimiters)
    config.read_file(file)
    return config


def save_config(config: ConfigParser, file: TextIO) -> None:
    """Save `config` to the `file`."""
    config.write(file)


@dataclass
class Field:
    section: str = ""
    name: str = ""
    value: str = ""

    @classmethod
    def from_string(cls, raw_string: str, *, without_value: bool = False) -> Self:
        """Create instance from `raw_string`."""
        section, sep, rest = raw_string.partition(".")
        if not sep:
            raise ValueError("invalid string format")

        if without_value:
            return cls(section=section.strip(), name=rest.strip())

        name, sep, value = rest.partition("=")
        if not sep:
            raise ValueError("invalid string format")

        return cls(section.strip(), name.strip(), value.strip())


def update_config_fields(config: ConfigParser, fields: list[Field]) -> None:
    """Update (override) config with **values** from the **list**."""
    for field in fields:
        if not config.has_section(field.section):
            config.add_section(field.section)

        config.set(field.section, field.name, field.value)


def remove_config_fields(config: ConfigParser, fields: list[Field]) -> None:
    """Update (override) config with **values** from the **list**."""
    for field in fields:
        if config.has_section(field.section) and config.has_option(field.section, field.name):
            config.remove_option(field.section, field.name)
