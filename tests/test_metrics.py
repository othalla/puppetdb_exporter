from unittest.mock import MagicMock
from prometheus_client import REGISTRY

from puppetdb_exporter.metrics import MetricsRender


class TestMetricsRender:
    @staticmethod
    def test_it_set_the_nodes_registered_gauge_metric():
        get_nodes = MagicMock(name='get_config',
                              return_value=['node1', 'node2'])
        metrics = MetricsRender(get_nodes)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_registered') == 2
