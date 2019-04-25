from unittest.mock import MagicMock, patch

import pytest

from puppetdb_exporter.puppetdb import FactNotFoundException, check_fact_path


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
