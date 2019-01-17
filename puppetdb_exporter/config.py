from configparser import ConfigParser
from os import environ

CONFIG = None


def get_config(configuration_parser=ConfigParser):
    configuration = configuration_parser()
    configuration.read(_read_config_files())
    global CONFIG
    return {}


def _read_config_files() -> str:
    if 'CONFIG_FILE' in environ:
        return environ['CONFIG_FILE']
