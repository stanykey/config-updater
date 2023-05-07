from dataclasses import astuple
from pathlib import Path
from unittest import main
from unittest import TestCase

from config_updater.arguments import get_arguments


class ArgumentsTest(TestCase):
    def test_get_arguments_basic(self) -> None:
        args = get_arguments(["fake-file", "key1=value1", "key2=value2", "key3=value3"])
        self.assertNotEqual("fake-file", args.file)
        self.assertEqual(Path("fake-file"), args.file)
        self.assertEqual(3, len(args.fields))

        with self.assertRaises(SystemExit):
            get_arguments(["fake-file-arg-only"])

        with self.assertRaises(ValueError):
            get_arguments(["fake-file-arg", "key-only"])

        with self.assertRaises(ValueError):
            get_arguments(["fake-file-arg", "key1=value1", "key-only"])

    def test_get_arguments_parse_values(self) -> None:
        args = get_arguments(["fake-file", "key1=value1", "key2=", "key3=key4=value3"])

        self.assertEqual(3, len(args.fields))
        self.assertEqual(("key1", "value1"), astuple(args.fields[0]))
        self.assertEqual(("key2", ""), astuple(args.fields[1]))
        self.assertEqual(("key3", "key4=value3"), astuple(args.fields[2]))


if __name__ == "__main__":
    main()
