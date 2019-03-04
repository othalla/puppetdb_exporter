from typing import Any, Iterator, Union

from pypuppetdb import BaseAPI, connect
from pypuppetdb.types import Node

from puppetdb_exporter.config import get_config


def _get_puppetdb_connexion() -> BaseAPI:
    config = get_config()['main']
    return connect(host=config['PUPPETDB_HOST'],
                   port=config['PUPPETDB_PORT'],
                   ssl_verify=config['PUPPETDB_SSL_VERIFY'],
                   ssl_key=config['PUPPETDB_KEY'],
                   ssl_cert=config['PUPPETDB_CERT'],
                   protocol=config['PUPPETDB_PROTO'])


def get_nodes() -> Union[Any, Iterator[Node]]:
    database = _get_puppetdb_connexion()
    return database.nodes(with_status=True)
