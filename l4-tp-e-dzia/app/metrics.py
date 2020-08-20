"""Metrics file."""

from flask import Flask, Response
from prometheus_client import multiprocess, generate_latest, \
    CollectorRegistry, CONTENT_TYPE_LATEST

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    """Metrics collector.

    :return: response
    """
    collector_registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(collector_registry)
    data = generate_latest(collector_registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
