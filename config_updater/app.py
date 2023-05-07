"""Simple tool to update/override cfg (ini) files from build scripts or CI pipelines via parameters."""
from argparse import Action
from argparse import ArgumentParser
from argparse import Namespace
from configparser import ConfigParser
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from sys import argv
from sys import stderr
from typing import Generator
from typing import List
from typing import Optional
from typing import Sequence
from typing import TextIO
from typing import Union


@dataclass
class Field:
    name: str
    value: str = ""


class ParseField(Action):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Union[str, Sequence[str], None],
        option_string: Optional[str] = None,
    ) -> None:
        if values is None:
            raise ValueError("field value is None")

        fields = []
        for value in values:
            key, sep, value = value.partition("=")
            if not sep:
                raise ValueError("invalid field value format")

            fields.append(Field(key, value))

        setattr(namespace, self.dest, fields)


@dataclass
class Arguments:
    file: Path
    fields: List[Field]


class CaseSensitiveConfigParser(ConfigParser):
    def optionxform(self, option_str: str) -> str:
        return option_str


def get_arguments(args: Sequence[str]) -> Arguments:
    """Parse command-line arguments and return them."""
    parser = ArgumentParser(prog="config-updater")
    parser.add_argument("file", type=Path, help="Config filename")
    parser.add_argument(
        "params",
        action=ParseField,
        metavar="key=value",
        nargs="+",
        help="List of key-value pairs to override config values",
    )

    options = parser.parse_args(args)
    return Arguments(file=options.file, fields=options.params)


def load_config(file: TextIO, delimiters: Sequence[str] = ("=",)) -> ConfigParser:
    """Load config from the `file`."""
    config = CaseSensitiveConfigParser(delimiters=delimiters)
    config.read_file(file)
    return config


def update_config(config: ConfigParser, values: List[Field]) -> None:
    """Update (override) config with **values** from the **list**."""
    for pair in values:
        for section in config.sections():
            if pair.name in config.options(section):
                config.set(section, pair.name, pair.value)


def save_config(config: ConfigParser, file: TextIO) -> None:
    """Save `config` to the `file`."""
    config.write(file)


@contextmanager
def config_file(file: Path) -> Generator[ConfigParser, None, None]:
    """Simple context manager to load/save config files."""
    with open(file, encoding="utf-8") as io:
        config = load_config(io)

    try:
        yield config
    except RuntimeError:
        return

    with open(file, "w", encoding="utf-8") as io:
        save_config(config, io)


def main() -> None:
    """Application entry point."""
    try:
        args = get_arguments(argv[1:])
    except ValueError as error:
        print(error, file=stderr)
        exit(1)

    with config_file(args.file) as config:
        update_config(config, args.fields)


if __name__ == "__main__":
    main()
