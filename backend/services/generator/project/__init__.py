import os

from flask import Flask


def create_app(script_info=None):
    # instantiate webapp
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprint
    from project.api.generator import generator_blueprint
    app.register_blueprint(generator_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app