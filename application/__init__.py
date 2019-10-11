import logging

from flask import current_app, Flask


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        db_api = get_db_api()
        db_api.init_app(app)

    # Register the Bookshelf CRUD blueprint.
    from .crud import crud
    app.register_blueprint(crud)

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app


def get_db_api():
    model_backend = current_app.config['DATA_BACKEND']
    if model_backend == 'mongodb':
        from application.api import db_api
        return db_api
    else:
        raise ValueError(
            "No appropriate databackend configured. "
            "Please specify datastore, cloudsql, or mongodb")
