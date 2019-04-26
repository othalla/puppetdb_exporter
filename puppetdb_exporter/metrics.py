from threading import Thread
from typing import Callable, Dict, Iterator, List, Union

from prometheus_client import Gauge
from pypuppetdb.types import Node

from puppetdb_exporter.config import Configuration
from puppetdb_exporter.puppetdb import get_fact, get_nodes

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
                List[Dict[str, Union[str, int]]]] = get_fact) -> None:
        Thread.__init__(self)
        self._configuration = configuration
        self._node_provider = node_provider
        self._fact_provider = fact_provider

    def run(self) -> None:
        self._generate_nodes_metrics()
        if self._configuration.fact_list:
            self._generate_facts_metrics()

    def _generate_facts_metrics(self) -> None:
        global GAUGE_FACTS  # pylint: disable=global-statement
        for fact_path in self._configuration.fact_list:
            formatted_fact = fact_path.replace('.', '_')
            facts = self._fact_provider(fact_path,
                                        self._configuration)
            GAUGE_FACTS[formatted_fact] = Gauge(
                f'puppetdb_fact_{formatted_fact}',
                'some gauge',
                labelnames=['value'])
            for fact in facts:
                GAUGE_FACTS[formatted_fact].labels(
                    value=fact['value']).set(fact['count'])

    def _generate_nodes_metrics(self) -> None:
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
