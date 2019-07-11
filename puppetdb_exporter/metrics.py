from threading import Thread
from typing import Callable, Dict, List, Union

from prometheus_client import Gauge
from pypuppetdb.types import Node

from puppetdb_exporter.config import Configuration
from puppetdb_exporter.puppetdb import get_environments, get_fact, get_nodes

GAUGE_NODES = Gauge('puppetdb_nodes_registered',
                    'Description of gauge',
                    labelnames=['environment'])
GAUGE_STATUS = Gauge('puppetdb_nodes_status',
                     'desc',
                     labelnames=['status', 'environment'])
GAUGE_FACTS: Dict[str, Gauge] = {}


class MetricsRender(Thread):
    def __init__(
            self,
            configuration: Configuration,
            node_provider: Callable[
                [str, Configuration],
                List[Node]] = get_nodes,
            fact_provider: Callable[
                [str, str, Configuration],
                List[Dict[str, Union[str, int]]]] = get_fact,
            environments_provider: Callable[
                [Configuration],
                List[str]] = get_environments) -> None:
        Thread.__init__(self)
        self._configuration = configuration
        self._node_provider = node_provider
        self._fact_provider = fact_provider
        self._environments_provider = environments_provider

    def run(self) -> None:
        environments = self._environments_provider(self._configuration)
        for environment in environments:
            self._generate_nodes_metrics(environment)
            if self._configuration.fact_list:
                self._generate_facts_metrics(environment)

    def _generate_facts_metrics(self, environment: str) -> None:
        global GAUGE_FACTS  # pylint: disable=global-statement
        for fact in self._configuration.fact_list:
            formatted_fact = fact.replace('.', '_')
            fact_results = self._fact_provider(fact,
                                               environment,
                                               self._configuration)
            if formatted_fact not in GAUGE_FACTS:
                GAUGE_FACTS[formatted_fact] = Gauge(
                    f'puppetdb_fact_{formatted_fact}',
                    'some gauge',
                    labelnames=['value', 'environment'])
            for fact_result in fact_results:
                GAUGE_FACTS[formatted_fact].labels(
                    value=fact_result['value'], environment=environment).set(
                        fact_result['count'])

    def _generate_nodes_metrics(self, environment: str) -> None:
        node_number = 0
        nodes = self._node_provider(environment, self._configuration)
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
                status_values[node.status.value] += 1
            except KeyError:
                continue
        GAUGE_NODES.labels(environment=environment).set(node_number)
        for status, value in status_values.items():
            GAUGE_STATUS.labels(status=status,
                                environment=environment).set(value)
