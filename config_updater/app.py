"""Simple tool to update/override cfg (ini) files from build scripts or CI pipelines via parameters."""

from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path
from sys import exit
from typing import Generator

from click import argument
from click import echo
from click import group
from click import pass_context
from click import pass_obj

from config_updater.config_reader import Field
from config_updater.config_reader import load_config
from config_updater.config_reader import remove_config_fields
from config_updater.config_reader import save_config
from config_updater.config_reader import update_config_fields


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


@group(options_metavar="")
@argument("file", type=Path)
@pass_context
def cli(ctx: object, file: Path) -> None:
    """A simple tool to update/override cfg (ini) files."""
    try:
        file = file.resolve(strict=True)
    except FileNotFoundError:
        log_error(f"config file ({file}) is missing")
        exit(1)

    # don't change the attribute name (obj)
    setattr(ctx, "obj", file)  # noqa: B010 (it's the `click` framework requirement)


@cli.command(name="update", options_metavar="")
@argument("params", nargs=-1, type=str, required=True, metavar="<SECTION.NAME=VALUE>...")
@pass_obj
def update_command(file: Path, params: list[str]) -> None:
    """Update (override) or add config fields."""
    try:
        fields = [Field.from_string(field_string) for field_string in params]
        with config_file(file) as config:
            update_config_fields(config, fields)
    except RuntimeError as ex:
        log_error(f"Error: {ex}")
        exit(1)


@cli.command(name="remove", options_metavar="")
@argument("params", nargs=-1, type=str, required=True, metavar="<SECTION.NAME>...")
@pass_obj
def remove_command(file: Path, params: list[str]) -> None:
    """Remove config fields if existed."""
    try:
        fields = [Field.from_string(field_str, without_value=True) for field_str in params]
        with config_file(file) as config:
            remove_config_fields(config, fields)
    except RuntimeError as ex:
        log_error(f"Error: {ex}")
        exit(1)


if __name__ == "__main__":
    cli()
