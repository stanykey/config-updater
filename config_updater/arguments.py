"""Application command-line arguments parser."""
from argparse import Action
from argparse import ArgumentParser
from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Optional
from typing import Sequence
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


def get_arguments(args: Sequence[str], description: Optional[str] = None) -> Arguments:
    """Parse command-line arguments and return them."""
    parser = ArgumentParser(prog="config-updater", description=description)
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
