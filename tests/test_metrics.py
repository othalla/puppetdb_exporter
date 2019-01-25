from unittest.mock import MagicMock
from prometheus_client import REGISTRY

from puppetdb_exporter.metrics import MetricsRender


NODE1 = MagicMock(name='node1', status='unchanged')
NODE2 = MagicMock(name='node2', status='changed')
NODE3 = MagicMock(name='node3', status='changed')
BAD_NODE = MagicMock(name='node3', status='unknown')


class TestMetricsRender:
    @staticmethod
    def test_it_set_the_nodes_registered_gauge_metric():
        get_nodes = MagicMock(name='get_config',
                              return_value=[NODE1, NODE2])
        metrics = MetricsRender(get_nodes)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_registered') == 2

    @staticmethod
    def test_it_set_the_nodes_by_status_gauge_metric():
        get_nodes = MagicMock(name='get_config',
                              return_value=[NODE1, NODE2, NODE3])
        metrics = MetricsRender(get_nodes)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'changed'}) == 2
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'unchanged'}) == 1
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'failed'}) == 0

    @staticmethod
    def test_with_unknown_node_status():
        get_nodes = MagicMock(name='get_config',
                              return_value=[BAD_NODE])
        metrics = MetricsRender(get_nodes)
        metrics.run()
