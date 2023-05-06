"""Simple tool to update/override cfg (ini) files from build scripts or CI pipelines via parameters."""
from argparse import ArgumentParser
from argparse import Namespace
from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path
from sys import argv
from typing import Generator
from typing import List
from typing import Tuple


def get_arguments() -> Namespace:
    """Parse command-line arguments and return them."""
    parser = ArgumentParser(prog="config-updater")
    parser.add_argument("file", type=Path, help="Config filename")
    parser.add_argument(
        "params",
        type=str,
        metavar="key=value",
        nargs="+",
        help="List of key-value pairs to override config values",
    )
    return parser.parse_args(argv[1:])


def parse_values(raw_values: List[str]) -> List[Tuple[str, str]]:
    """Parse `raw_values` into list of tuples (key, value)."""
    return [(key, value) for raw_value in raw_values for key, _, value in [raw_value.partition("=")]]


def load_config(file: Path) -> ConfigParser:
    """Load config from the `file`."""
    config = ConfigParser()
    config.read(file, encoding="utf-8")
    return config


def update_config(config: ConfigParser, values: List[Tuple[str, str]]) -> None:
    """Update (override) config with **values** from the **list**."""
    # TODO: add main magic here
    pass


def save_config(config: ConfigParser, file: Path) -> None:
    """Save `config` to the `file`."""
    with open(file, "w", encoding="utf-8") as cfg_file:
        config.write(cfg_file)


@contextmanager
def config_file(file: Path) -> Generator[ConfigParser, None, None]:
    config = load_config(file)
    try:
        yield config
    finally:
        save_config(config, file)


def main() -> None:
    """Application entry point."""
    args = get_arguments()
    values = parse_values(raw_values=args.params)
    with config_file(args.file) as config:
        update_config(config, values)


if __name__ == "__main__":
    main()
