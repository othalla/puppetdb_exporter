from unittest.mock import MagicMock

from prometheus_client import REGISTRY

from puppetdb_exporter.metrics import MetricsRender
from puppetdb_exporter.node import Node, Status

NODE1 = Node('node1', Status.UNCHANGED)
NODE2 = Node('node2', Status.CHANGED)
NODE3 = Node('node3', Status.CHANGED)


class TestMetricsRender:
    @staticmethod
    def test_it_set_the_nodes_registered_gauge_metric():
        get_nodes = MagicMock(name='get_nodes',
                              return_value=[NODE1, NODE2])
        get_environments = MagicMock(name="get_environments",
                                     return_value=['env1'])
        metrics = MetricsRender(configuration=MagicMock(name='Configuration',
                                                        fact_list=[]),
                                node_provider=get_nodes,
                                environments_provider=get_environments)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_registered',
                                         {'environment': 'env1'}) == 2

    @staticmethod
    def test_it_set_the_nodes_registered_gauge_metric_with_two__environments():
        get_nodes = MagicMock(name='get_nodes',
                              return_value=[NODE1, NODE2])
        get_environments = MagicMock(name="get_environments",
                                     return_value=['env1', 'env2'])
        metrics = MetricsRender(configuration=MagicMock(name='Configuration',
                                                        fact_list=[]),
                                node_provider=get_nodes,
                                environments_provider=get_environments)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_registered',
                                         {'environment': 'env1'}) == 2
        assert REGISTRY.get_sample_value('puppetdb_nodes_registered',
                                         {'environment': 'env2'}) == 2

    @staticmethod
    def test_it_set_the_nodes_by_status_gauge_metric():
        get_nodes = MagicMock(name='get_nodes',
                              return_value=[NODE1, NODE2, NODE3])
        get_environments = MagicMock(name="get_environments",
                                     return_value=['env1'])
        metrics = MetricsRender(configuration=MagicMock(name='Configuration',
                                                        fact_list=[]),
                                node_provider=get_nodes,
                                environments_provider=get_environments)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'changed',
                                          'environment': 'env1'}) == 2
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'unchanged',
                                          'environment': 'env1'}) == 1
        assert REGISTRY.get_sample_value('puppetdb_nodes_status',
                                         {'status': 'failed',
                                          'environment': 'env1'}) == 0

    @staticmethod
    def test_with_an_optional_fact_set_gauge_metric():
        get_nodes = MagicMock(name='get_nodes', return_value=[NODE1, NODE2])
        get_environments = MagicMock(name="get_environments",
                                     return_value=['env1'])
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
                                  fact_list=["kernelrelease", "os.name"])
        metrics = MetricsRender(configuration=configuration,
                                node_provider=get_nodes,
                                fact_provider=get_fact,
                                environments_provider=get_environments)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_fact_kernelrelease',
                                         {'value': '3.10.250',
                                          'environment': 'env1'}) == 10
        assert REGISTRY.get_sample_value('puppetdb_fact_kernelrelease',
                                         {'value': '3.10.290',
                                          'environment': 'env1'}) == 15
        assert REGISTRY.get_sample_value('puppetdb_fact_os_name',
                                         {'value': 'foo',
                                          'environment': 'env1'}) == 1
        assert REGISTRY.get_sample_value('puppetdb_fact_os_name',
                                         {'value': 'bar',
                                          'environment': 'env1'}) == 5

    @staticmethod
    def test_with_an_optional_fact_but_empty_puppetdb_response():
        get_nodes = MagicMock(name='get_nodes', return_value=[NODE1, NODE2])
        get_environments = MagicMock(name="get_environments",
                                     return_value=['env1'])
        get_fact = MagicMock(name='get_fact', return_value=[])
        configuration = MagicMock(name='configuration', fact_list=["badfact"])
        metrics = MetricsRender(configuration=configuration,
                                node_provider=get_nodes,
                                fact_provider=get_fact,
                                environments_provider=get_environments)
        metrics.run()
        assert REGISTRY.get_sample_value('puppetdb_fact_badfact') is None
