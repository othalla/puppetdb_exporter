from unittest.mock import MagicMock
from prometheus_client import REGISTRY

from puppetdb_exporter.metrics import MetricsRender


class TestMetricsRender:
    @staticmethod
    def test_it_set_the_nodes_registered_gauge_metric():
        node1 = MagicMock(name='node1', status='unchanged')
        node2 = MagicMock(name='node2', status='changed')
        node3 = MagicMock(name='node3', status='changed')
        get_nodes = MagicMock(name='get_config',
                              return_value=[node1, node2, node3])
        metrics = MetricsRender(get_nodes)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_registered') == 3

    @staticmethod
    def test_it_set_the_nodes_by_status_gauge_metric():
        node1 = MagicMock(name='node1', status='unchanged')
        node2 = MagicMock(name='node2', status='changed')
        node3 = MagicMock(name='node3', status='changed')
        get_nodes = MagicMock(name='get_config',
                              return_value=[node1, node2, node3])
        metrics = MetricsRender(get_nodes)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'changed'}) == 2
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'unchanged'}) == 1
