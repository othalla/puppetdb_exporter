from typing import Callable
from threading import Thread

from prometheus_client import Gauge

from puppetdb_exporter.puppetdb import get_nodes


gauge_nodes = Gauge('puppetdb_nodes_registered', 'Description of gauge')


class MetricsRender(Thread):
    def __init__(self, node_provider: Callable = get_nodes) -> None:
        Thread.__init__(self)
        self._node_provider = node_provider

    def run(self) -> None:
        self._generate_metrics()

    def _generate_metrics(self):
        self._node_provider()
