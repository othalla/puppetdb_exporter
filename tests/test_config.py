from os import environ, path
from unittest.mock import patch
from pathlib import Path

import pytest

from puppetdb_exporter.config import (ConfigurationException, Configuration)

FIXTURE_CONFIG = path.join(Path(__file__).absolute().parent,
                           'fixtures',
                           'config.ini')


class TestConfiguration:
    @staticmethod
    def test_with_no_config_file_environment_variable():
        with pytest.raises(ConfigurationException,
                           match=r'No configuration file provided.*'):
            _ = Configuration()

    @staticmethod
    def test_with_empty_config_file_environment_variale():
        with patch.dict(environ, {'CONFIG_FILE': ''}):
            with pytest.raises(ConfigurationException,
                               match=r'No configuration file provided.*'):
                _ = Configuration()

    @staticmethod
    def test_with_if_config_file_cannot_be_read():
        with patch.dict(environ, {'CONFIG_FILE': '/bad/path'}):
            with pytest.raises(ConfigurationException,
                               match=r'Failed to load configuration.*'):
                _ = Configuration()

    @staticmethod
    def test_it_load_setting():
        with patch.dict(environ, {'CONFIG_FILE': FIXTURE_CONFIG}):
            configuration = Configuration()
            assert configuration.puppetdb_host == 'somehost'
