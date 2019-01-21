from configparser import ConfigParser
from unittest.mock import create_autospec, patch

from puppetdb_exporter.config import get_config


class TestConfig:
    @staticmethod
    def test_it_load_given_config_file_from_environment_variable():
        config_parser = create_autospec(ConfigParser)
        with patch.dict('os.environ', {'CONFIG_FILE': '/path/config'}):
            get_config(config_parser=config_parser)
            config_parser.return_value.read.assert_called_once_with(
                ['/path/config'])

    @staticmethod
    def test_it_load_config_file_from_default_files():
        config_parser = create_autospec(ConfigParser)
        get_config(config_parser=config_parser)
        config_parser.return_value.read.assert_called_once_with(
            ['/etc/puppetdb_exporter/config.ini',
             '.config/puppetdb_exporter/config.ini',
             'config.ini']
        )
