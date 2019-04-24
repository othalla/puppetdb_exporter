from unittest.mock import MagicMock, patch

from puppetdb_exporter.puppetdb import get_fact_path


def test_get_fact_path_perform_correct_puppetdb_query():
    with patch('puppetdb_exporter.puppetdb.connect') as mock_connect:
        get_fact_path('fact.path',
                      configuration=MagicMock(name='configurationn'))
        mock_connect.return_value.fact_paths.assert_called_once_with(
            query='["=", "path", ["fact", "path"]]')
