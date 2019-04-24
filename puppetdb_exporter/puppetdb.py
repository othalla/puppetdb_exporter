from typing import Any, Iterator, Union

from pypuppetdb import BaseAPI, connect
from pypuppetdb.types import Node

from puppetdb_exporter.config import Configuration


def _get_puppetdb_connexion(configuration: Configuration) -> BaseAPI:
    return connect(host=configuration.puppetdb_host,
                   port=configuration.puppetdb_port,
                   ssl_verify=configuration.puppetdb_ssl_verify,
                   ssl_key=configuration.puppetdb_ssl_key,
                   ssl_cert=configuration.puppetdb_ssl_cert,
                   protocol=configuration.puppetdb_proto)


def get_nodes(configuration: Configuration) -> Union[Any, Iterator[Node]]:
    database = _get_puppetdb_connexion(configuration)
    return database.nodes(with_status=True)
