from configparser import ConfigParser, Error
from os import environ
from typing import List


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

    @property
    def puppetdb_ssl_verify(self) -> str:
        return self._configuration.get('puppetdb', 'ssl_verify')

    @property
    def puppetdb_ssl_key(self) -> str:
        return self._configuration.get('puppetdb', 'ssl_key')

    @property
    def puppetdb_ssl_cert(self) -> str:
        return self._configuration.get('puppetdb', 'ssl_cert')

    @property
    def puppetdb_proto(self) -> str:
        return self._configuration.get('puppetdb', 'proto')

    @property
    def fact_list(self) -> List[str]:
        try:
            raw_fact_list = self._configuration.get('optional', 'fact_list')
        except Error:
            return []
        return raw_fact_list.split(' ')
