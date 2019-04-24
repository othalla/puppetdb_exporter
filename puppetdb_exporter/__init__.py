import time

from prometheus_client import start_http_server

from puppetdb_exporter.config import Configuration
from puppetdb_exporter.metrics import MetricsRender


def _loop() -> None:
    configuration = Configuration()
    while True:
        metrics = MetricsRender(configuration=configuration)
        metrics.start()
        time.sleep(15)
        metrics.join()


def main() -> None:
    start_http_server(8000)
    _loop()


if __name__ == '__main__':
    main()
