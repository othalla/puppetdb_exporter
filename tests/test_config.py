from configparser import ConfigParser
from unittest.mock import create_autospec, patch

import pytest

from puppetdb_exporter.config import (get_config,
                                      ConfigurationException,
                                      SETTINGS)


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

    @staticmethod
    def test_it_cannot_load_configuration_without_main_section():
        with patch.dict('os.environ', {'CONFIG_FILE': '/path/config/ko'}):
            with pytest.raises(ConfigurationException,
                               match='Missing main section in config file.'):
                get_config()

    @staticmethod
    def test_it_cannot_load_configuration_without_puppetdb_settings():
        config_parser = create_autospec(ConfigParser)
        config_parser.return_value.has_option.return_value = False
        with pytest.raises(ConfigurationException,
                           match=r'Missing .* setting in config file.'):
            get_config(config_parser=config_parser)

    @staticmethod
    def test_it_load_configuration_properly():
        config_parser = create_autospec(ConfigParser)
        config_parser.return_value.has_option.return_value = True
        get_config(config_parser=config_parser)
        assert config_parser.return_value.has_option.call_count == len(SETTINGS)
        for setting in SETTINGS:
            config_parser.return_value.has_option.assert_any_call('main',
                                                                  setting)
