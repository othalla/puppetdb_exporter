from threading import Thread

from prometheus_client import Gauge

from puppetdb_exporter.puppetdb import get_nodes


gauge_nodes = Gauge('puppetdb_nodes_registered', 'Description of gauge')
gauge_status = Gauge('puppetdb_nodes_status', 'desc', labelnames=['status'])


NODE_STATUS = [
    'changed', 'failed', 'noop', 'skipped', 'unchanged', 'unreported'
]
PUPPETDB_CONNEXION = None


class MetricsRender(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self._generate_metrics()

    def _generate_metrics(self):
        nodes = get_nodes()
        for node_status in NODE_STATUS:
            gauge_status.labels(status=node_status).set(0)
        assert nodes
