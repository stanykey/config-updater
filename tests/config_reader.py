from io import StringIO
from unittest import main
from unittest import TestCase

from config_updater.app import Field
from config_updater.app import update_config
from config_updater.config_reader import load_config
from config_updater.config_reader import save_config


TEST_CONFIG = """
[log4cplus]
threadPoolSize = 1
rootLogger = TRACE, console, file
logger.Service::WRTC = WARN
logger.Service::Onvif = DEBUG
appender.console = log4cplus::ConsoleAppender
appender.console.AsyncAppend = false
appender.console.ImmediateFlush = false
appender.console.layout = log4cplus::PatternLayout
appender.console.layout.ConversionPattern = %D{%m/%d/%y %H:%M:%S} %-5p %c [%x] - %m%n
appender.file = log4cplus::FileAppender
appender.file.AsyncAppend = false
appender.file.ImmediateFlush = false
appender.file.layout = log4cplus::PatternLayout
appender.file.layout.ConversionPattern = %D{%m/%d/%y %H:%M:%S} %-5p %c [%x] - %m%n
appender.file.File = vmsapp.log

[general]
depot.link =
depot.tmpLink =
blackholePath =
platform = null
service.0 = keepalive

"""


class ConfigTest(TestCase):
    def test_basics(self) -> None:
        with StringIO(TEST_CONFIG) as input_file:
            config = load_config(input_file)

        self.assertTrue("log4cplus" in config.sections())
        self.assertEqual("TRACE, console, file", config.get("log4cplus", "rootLogger"))
        self.assertEqual("WARN", config.get("log4cplus", "logger.Service::WRTC"))
        self.assertEqual("DEBUG", config.get("log4cplus", "logger.Service::Onvif"))

        self.assertTrue("general" in config.sections())
        self.assertEqual("", config.get("general", "depot.link"))
        self.assertEqual("null", config.get("general", "platform"))
        self.assertEqual("keepalive", config.get("general", "service.0"))

    def test_update_config(self) -> None:
        with StringIO(TEST_CONFIG) as input_file:
            config = load_config(input_file)

        fields = [
            Field(name="depot.link", value="/media/fake-depot-path"),
            Field(name="platform", value="ssr338"),
        ]
        update_config(config, fields)

        output_file = StringIO()
        save_config(config, output_file)
        output_file.seek(0)
        saved_raw_text = output_file.read()
        self.assertTrue("/media/fake-depot-path" in saved_raw_text)
        self.assertTrue("ssr338" in saved_raw_text)

        output_file.seek(0)
        config = load_config(output_file)
        self.assertEqual("/media/fake-depot-path", config.get("general", "depot.link"))
        self.assertEqual("ssr338", config.get("general", "platform"))


if __name__ == "__main__":
    main()
