"""Tweaked version of ConfigParser that supports case-sensitive keys."""

from configparser import ConfigParser
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
