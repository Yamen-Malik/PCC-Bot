from threading import Thread
from flask import Flask


app = Flask("")


@app.route("/")
def home():
    """Main Flask endpoint. Used to report server status."""

    return "server is alive"


def run():
    """Run Flask application"""

    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    """Starts a new thread with the Flask application"""

    thread = Thread(target=run, daemon=True)
    thread.start()
