from configparser import ConfigParser
from os import environ
from typing import List, Type

CONFIG = None


class ConfigurationException(Exception):
    pass


def get_config(
        config_parser: Type[ConfigParser] = ConfigParser) -> ConfigParser:
    configuration = config_parser()
    configuration.read(_read_config_files())
    if not configuration.has_section('main'):
        raise ConfigurationException
    return configuration


def _read_config_files() -> List[str]:
    if 'CONFIG_FILE' in environ:
        return [environ['CONFIG_FILE']]
    return ['/etc/puppetdb_exporter/config.ini',
            '.config/puppetdb_exporter/config.ini',
            'config.ini']
