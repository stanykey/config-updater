"""Simple tool to update/override cfg (ini) files from build scripts or CI pipelines via parameters."""
from argparse import ArgumentParser
from argparse import Namespace
from pathlib import Path
from sys import argv


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


def main() -> None:
    """Application entry point."""
    args = get_arguments()
    print(args.file)
    print(args.params)


if __name__ == "__main__":
    main()
