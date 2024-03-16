"""Simple tool to update/override cfg (ini) files from build scripts or CI pipelines via parameters."""

from configparser import ConfigParser
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from sys import exit
from typing import Generator
from typing import List

from click import argument
from click import command
from click import echo

from config_updater.config_reader import load_config
from config_updater.config_reader import save_config


@dataclass
class Field:
    name: str = ""
    value: str = ""

    @classmethod
    def from_string(cls, kv_pair: str) -> "Field":
        name, sep, value = kv_pair.partition("=")
        if not sep:
            raise ValueError("invalid field value format")

        return cls(name, value)


def log_info(message: str) -> None:
    echo(message)


def log_error(message: str) -> None:
    echo(message, err=True)


@contextmanager
def config_file(file: Path) -> Generator[ConfigParser, None, None]:
    """Simple context manager to load/save config files."""
    with open(file, encoding="utf-8") as io:
        config = load_config(io)

    yield config

    with open(file, "w", encoding="utf-8") as io:
        save_config(config, io)


def update_config(config: ConfigParser, values: List[Field]) -> None:
    """Update (override) config with **values** from the **list**."""
    for pair in values:
        for section in config.sections():
            if pair.name in config.options(section):
                config.set(section, pair.name, pair.value)


@command()
@argument("file", type=Path)
@argument("params", nargs=-1, type=str, required=True)
def main(file: Path, params: List[str]) -> int:
    """Application entry point."""
    try:
        file = file.resolve(strict=True)
    except FileNotFoundError:
        log_error(f"config file ({file}) is missing")
        return 1

    try:
        fields = [Field.from_string(kv_pair) for kv_pair in params]
        with config_file(file) as config:
            update_config(config, fields)
    except RuntimeError as ex:
        log_error(f"error: {ex}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
