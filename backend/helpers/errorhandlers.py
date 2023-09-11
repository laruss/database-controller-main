import flask

from backend.helpers.utils import not_found_response, response


def register_errorhandlers(app: flask.Flask):
    exc = 500 if app.config["DEBUG"] else Exception

    @app.errorhandler(404)
    def page_not_found(e):
        return not_found_response({"error": "route not found"})

    @app.errorhandler(exc)
    def internal_server_error(e):
        return response({"error": str(e)}, status=500)
