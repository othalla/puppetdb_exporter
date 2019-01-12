import hug
from falcon import HTTP_200

import puppetdb_exporter.app as app


def tests_metrics():
    response = hug.test.get(app, 'metrics')
    assert response.status == HTTP_200
