from configparser import ConfigParser
from os import environ

CONFIG_FILE_ERROR_MESSAGE = ('No configuration file provided. '
                             'You must set CONFIG_FILE environment variable.')


class ConfigurationException(Exception):
    pass


class Configuration():
    def __init__(self) -> None:
        self._configuration = ConfigParser()
        if 'CONFIG_FILE' not in environ or not environ['CONFIG_FILE']:
            raise ConfigurationException('No configuration file provided. '
                                         'You must set CONFIG_FILE '
                                         'environment variable.')
        if not self._configuration.read(environ['CONFIG_FILE']):
            raise ConfigurationException('Failed to load configuration file. '
                                         'You must provide a valide file '
                                         'in the CONFIG_FILE '
                                         'environment variale.')

    @property
    def puppetdb_host(self) -> str:
        return self._configuration.get('puppetdb', 'host')

    @property
    def puppetdb_port(self) -> int:
        return self._configuration.getint('puppetdb', 'port')
