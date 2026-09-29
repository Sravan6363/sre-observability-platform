from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests",
    ["endpoint"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)


@app.route("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()

    with REQUEST_LATENCY.labels(endpoint="/").time():
        return jsonify({
            "application": "SRE Observability Platform",
            "status": "running",
            "version": "1.0.0"
        })


@app.route("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()

    with REQUEST_LATENCY.labels(endpoint="/health").time():
        return jsonify({
            "status": "healthy"
        }), 200


@app.route("/slow")
def slow():
    REQUEST_COUNT.labels(endpoint="/slow").inc()

    with REQUEST_LATENCY.labels(endpoint="/slow").time():
        time.sleep(2)

        return jsonify({
            "message": "Response intentionally delayed",
            "delay": "2 seconds"
        })


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
