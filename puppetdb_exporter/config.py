from configparser import ConfigParser
from os import environ
from typing import List, Type

SETTINGS = [
    'puppetdb_host',
    'puppetdb_port',
    'puppetdb_ssl_verify',
    'puppetdb_key',
    'puppetdb_cert',
    'puppetdb_proto',
]


class ConfigurationException(Exception):
    pass


def get_config(
        config_parser: Type[ConfigParser] = ConfigParser) -> ConfigParser:
    configuration = config_parser()
    configuration.read(_read_config_files())
    _check_config_settings(configuration)
    return configuration


def _read_config_files() -> List[str]:
    if 'CONFIG_FILE' in environ:
        return [environ['CONFIG_FILE']]
    return ['/etc/puppetdb_exporter/config.ini',
            '.config/puppetdb_exporter/config.ini',
            'config.ini']


def _check_config_settings(configuration: ConfigParser) -> None:
    if not configuration.has_section('main'):
        raise ConfigurationException('Missing main section in config file.')
    for setting in SETTINGS:
        if not configuration.has_option('main', setting):
            raise ConfigurationException(f'Missing {setting} setting in '
                                         'config file.')
