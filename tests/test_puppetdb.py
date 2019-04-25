from unittest.mock import MagicMock, patch

import pytest

from puppetdb_exporter.puppetdb import (FactNotFoundException, check_fact_path,
                                        get_fact)


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
