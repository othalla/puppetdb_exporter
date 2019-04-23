from os import environ, path
from tempfile import NamedTemporaryFile
from unittest.mock import patch
from pathlib import Path

import pytest

from puppetdb_exporter.config import (ConfigurationException, Configuration)


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
    def test_it_load_setting_new():
        with NamedTemporaryFile() as temp_file:
            with open(temp_file.name, 'w') as file_descriptor:
                file_descriptor.write(
                    '[puppetdb]\n'
                    'host = lol\n')
            with patch.dict(environ, {'CONFIG_FILE': temp_file.name}):
                configuration = Configuration()
                assert configuration.puppetdb_host == 'lol'
