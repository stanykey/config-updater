"""Simple tool to update/override cfg (ini) files from build scripts or CI pipelines via parameters."""
from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path
from sys import argv
from sys import stderr
from typing import Generator
from typing import List

from config_updater.arguments import Field
from config_updater.arguments import get_arguments
from config_updater.config_reader import load_config
from config_updater.config_reader import save_config


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


def update_config(config: ConfigParser, values: List[Field]) -> None:
    """Update (override) config with **values** from the **list**."""
    for pair in values:
        for section in config.sections():
            if pair.name in config.options(section):
                config.set(section, pair.name, pair.value)


def main() -> None:
    """Application entry point."""
    try:
        args = get_arguments(argv[1:], __doc__)
    except ValueError as error:
        print(error, file=stderr)
        exit(1)

    with config_file(args.file) as config:
        update_config(config, args.fields)


if __name__ == "__main__":
    main()
