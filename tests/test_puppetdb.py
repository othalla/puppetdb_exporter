from unittest.mock import MagicMock, patch

import pytest
from pypuppetdb.types import Node as PuppetDBNode

from puppetdb_exporter.node import Node, Status
from puppetdb_exporter.puppetdb import (FactNotFoundException, check_fact_path,
                                        get_fact, get_nodes)


class TestGetNodes:
    @staticmethod
    def test_it_returns_a_list_of_nodes():
        with patch('puppetdb_exporter.puppetdb.connect') as mock_connect:
            mock_connect.return_value.nodes.return_value = iter([
                PuppetDBNode(MagicMock(name='api'),
                             'node1',
                             status_report='changed'),
                PuppetDBNode(MagicMock(name='api'),
                             'node2',
                             status_report='changed')
            ])
            nodes = get_nodes(configuration=MagicMock(name='configuration'))
            assert Node('node1', Status.CHANGED) in nodes
            assert Node('node2', Status.CHANGED) in nodes


class TestChecKFactPath:
    @staticmethod
    def test_it_perform_correct_puppetdb_query():
        with patch('puppetdb_exporter.puppetdb.connect') as mock_connect:
            check_fact_path('fact.path',
                            configuration=MagicMock(name='configurationn'))
            mock_connect.return_value.fact_paths.assert_called_once_with(
                query='["=", "path", ["fact", "path"]]')

    @staticmethod
    def test_if_fact_not_found():
        with patch('puppetdb_exporter.puppetdb.connect') as mock_connect:
            mock_connect.return_value.fact_paths.return_value = []
            with pytest.raises(FactNotFoundException):
                check_fact_path('fact.path',
                                configuration=MagicMock(name='configurationn'))

    @staticmethod
    def test_if_fact_found():
        with patch('puppetdb_exporter.puppetdb.connect'):
            check_fact_path('fact.path',
                            configuration=MagicMock(name='configurationn'))


class TestGetFact:
    @staticmethod
    def test_it_perform_correct_puppetdb_query():
        with patch('puppetdb_exporter.puppetdb.connect') as mock_connect:
            get_fact('fact.path',
                     configuration=MagicMock(name='configurationn'))
            mock_connect.return_value.fact_contents.assert_called_once_with(
                query=('["extract", [["function", "count"], "value"], '
                       '["=", "path", ["fact", "path"]], '
                       '["group_by", "value"]]'))

    @staticmethod
    def test_it_returns_the_fact_data():
        with patch('puppetdb_exporter.puppetdb.connect') as mock_connect:
            mock_connect.return_value.fact_contents.return_value = [
                {"value": "one", "count": 12}
            ]
            result = get_fact('fact.path',
                              configuration=MagicMock(name='configurationn'))
            assert result == [{"value": "one", "count": 12}]
