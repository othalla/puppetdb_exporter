import time

from prometheus_client import start_http_server

from puppetdb_exporter.metrics import MetricsRender


def _loop() -> None:
    while True:
        metrics = MetricsRender()
        metrics.start()
        time.sleep(15)
        metrics.join()


if __name__ == '__main__':
    start_http_server(8000)
    _loop()
