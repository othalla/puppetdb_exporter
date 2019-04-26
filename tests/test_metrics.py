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
        get_nodes = MagicMock(name='get_nodes',
                              return_value=[NODE1, NODE2])
        metrics = MetricsRender(configuration=MagicMock(name='Configuration',
                                                        fact_list=[]),
                                node_provider=get_nodes)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_registered') == 2

    @staticmethod
    def test_it_set_the_nodes_by_status_gauge_metric():
        get_nodes = MagicMock(name='get_nodes',
                              return_value=[NODE1, NODE2, NODE3])
        metrics = MetricsRender(configuration=MagicMock(name='Configuration',
                                                        fact_list=[]),
                                node_provider=get_nodes)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'changed'}) == 2
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'unchanged'}) == 1
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'failed'}) == 0

    @staticmethod
    def test_with_unknown_node_status():
        get_nodes = MagicMock(name='get_nodes',
                              return_value=[BAD_NODE])
        metrics = MetricsRender(configuration=MagicMock(name='Configuration',
                                                        fact_list=[]),
                                node_provider=get_nodes)
        metrics.run()

    @staticmethod
    def test_with_an_optional_fact_set_gauge_metric():
        get_nodes = MagicMock(name='get_nodes', return_value=[NODE1, NODE2])
        get_fact = MagicMock(name='get_fact', side_effect=[
            [
                {"value": "3.10.250", "count": 10},
                {"value": "3.10.290", "count": 15}
            ],
            [
                {"value": "foo", "count": 1},
                {"value": "bar", "count": 5}
            ]
        ])
        configuration = MagicMock(name='configuration',
                                  fact_list=["kernelrelease", "osname"])
        metrics = MetricsRender(configuration=configuration,
                                node_provider=get_nodes,
                                fact_provider=get_fact)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_fact_kernelrelease',
                                         {'value': '3.10.250'}) == 10
        assert REGISTRY.get_sample_value('puppetdb_fact_kernelrelease',
                                         {'value': '3.10.290'}) == 15
        assert REGISTRY.get_sample_value('puppetdb_fact_osname',
                                         {'value': 'foo'}) == 1
        assert REGISTRY.get_sample_value('puppetdb_fact_osname',
                                         {'value': 'bar'}) == 5
