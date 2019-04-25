from typing import Any, Dict, Iterator, List, Union

from pypuppetdb import BaseAPI, connect
from pypuppetdb.types import Node

from puppetdb_exporter.config import Configuration


class FactNotFoundException(Exception):
    pass


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


def check_fact_path(path: str, configuration: Configuration) -> None:
    database = _get_puppetdb_connexion(configuration)
    string_fact_path = '"' + path.replace('.', '", "') + '"'
    if not database.fact_paths(query=f'["=", "path", [{string_fact_path}]]'):
        raise FactNotFoundException


def get_fact(path: str, configuration: Configuration) -> List[
        Dict[str, Union[str, int]]]:
    database = _get_puppetdb_connexion(configuration)
    string_fact_path = '"' + path.replace('.', '", "') + '"'
    query = ('["extract", [["function", "count"], "value"], '
             f'["=", "path", [{string_fact_path}]], '
             '["group_by", "value"]]')
    return database.fact_contents(query=query)
