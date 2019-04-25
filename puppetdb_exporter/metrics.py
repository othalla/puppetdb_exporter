from threading import Thread
from typing import Callable, Dict, Iterator, Union

from prometheus_client import Gauge
from pypuppetdb.types import Node

from puppetdb_exporter.config import Configuration
from puppetdb_exporter.puppetdb import get_nodes, get_fact

GAUGE_NODES = Gauge('puppetdb_nodes_registered', 'Description of gauge')
GAUGE_STATUS = Gauge('puppetdb_nodes_status', 'desc', labelnames=['status'])
GAUGE_FACTS = {}


class MetricsRender(Thread):
    def __init__(
            self,
            configuration: Configuration,
            node_provider: Callable[
                [Configuration],
                Iterator[Node]] = get_nodes,
            fact_provider: Callable[
                [str, Configuration],
                Dict[str, Union[str, int]]] = get_fact) -> None:
        Thread.__init__(self)
        self._configuration = configuration
        self._node_provider = node_provider
        self._fact_provider = fact_provider

    def run(self) -> None:
        self._generate_node_metrics()
        if self._configuration.fact_list:
            self._generate_facts_metrics()

    def _generate_facts_metrics(self) -> None:
        global GAUGE_FACTS
        fact = self._fact_provider(self._configuration.fact_list[0],
                                   self._configuration)
        GAUGE_FACTS[self._configuration.fact_list[0]] = Gauge(
            f'puppetdb_fact_{self._configuration.fact_list[0]}',
            'some gauge',
            labelnames=['value'])
        GAUGE_FACTS[self._configuration.fact_list[0]].labels(
            value=fact[0]['value']).set(fact[0]['count'])

    def _generate_node_metrics(self) -> None:
        node_number = 0
        nodes = self._node_provider(self._configuration)
        status_values = {
            'changed': 0,
            'failed': 0,
            'noop': 0,
            'skipped': 0,
            'unchanged': 0,
            'unreported': 0,
        }
        for node in nodes:
            node_number += 1
            try:
                status_values[node.status] += 1
            except KeyError:
                continue
        GAUGE_NODES.set(node_number)
        for status, value in status_values.items():
            GAUGE_STATUS.labels(status=status).set(value)
