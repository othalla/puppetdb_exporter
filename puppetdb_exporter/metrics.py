from typing import Callable
from threading import Thread

from prometheus_client import Gauge

from puppetdb_exporter.puppetdb import get_nodes


GAUGE_NODES = Gauge('puppetdb_nodes_registered', 'Description of gauge')
GAUGE_STATUS = Gauge('puppetdb_nodes_status', 'desc', labelnames=['status'])


class MetricsRender(Thread):
    def __init__(self, node_provider: Callable = get_nodes) -> None:
        Thread.__init__(self)
        self._node_provider = node_provider

    def run(self) -> None:
        self._generate_metrics()

    def _generate_metrics(self) -> None:
        nodes = self._node_provider()
        GAUGE_NODES.set(len(nodes))
        status_values = {
            'changed': 0,
            'failed': 0,
            'noop': 0,
            'skipped': 0,
            'unchanged': 0,
            'unreported': 0,
        }
        for node in nodes:
            status_values[node.status] += 1
        for status_value in status_values:
            GAUGE_STATUS.labels(status=status_value).set(status_values[status_value])
