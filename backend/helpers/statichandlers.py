import os

import flask

import config


def register_statichandlers(app: flask.Flask):
    @app.route("/", defaults={"path": ""})
    def serve(path):
        if not os.path.exists(config.static_path):
            return flask.jsonify({"error": "Static folder not found"}), 500
        if path != "" and os.path.exists(config.static_path / path):
            return flask.send_from_directory(config.static_path, path)
        else:
            return flask.send_from_directory(config.static_path, "index.html")

    @app.route("/static/css/<path:path>")
    def send_css(path):
        return flask.send_from_directory(config.css_path, path)

    @app.route("/static/js/<path:path>")
    def send_js(path):
        return flask.send_from_directory(config.js_path, path)
