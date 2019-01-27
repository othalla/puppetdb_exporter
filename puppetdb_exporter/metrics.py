from typing import Callable, Iterator
from threading import Thread

from pypuppetdb.types import Node
from prometheus_client import Gauge

from puppetdb_exporter.puppetdb import get_nodes


GAUGE_NODES = Gauge('puppetdb_nodes_registered', 'Description of gauge')
GAUGE_STATUS = Gauge('puppetdb_nodes_status', 'desc', labelnames=['status'])


class MetricsRender(Thread):
    def __init__(
            self,
            node_provider: Callable[[], Iterator[Node]] = get_nodes) -> None:
        Thread.__init__(self)
        self._node_provider = node_provider

    def run(self) -> None:
        self._generate_metrics()

    def _generate_metrics(self) -> None:
        node_number = 0
        nodes = self._node_provider()
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
