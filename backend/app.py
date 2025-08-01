"""Run RetroBoard server."""

import os

from flask import Flask
from flask_restx import Api

from config import DevelopmentConfig, ProductionConfig
from routes.board_routes import (
    boards_ns,
    categories_ns,
    notes_ns,
    register_static_routes,
)

CONFIG = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}


def create_app(testing=False):
    """Create and configure the RetroBoard Flask app."""

    # Determine environment and load appropriate configuration
    env = os.environ.get("FLASK_ENV", "production").lower()
    static_folder_path = os.path.join(os.path.dirname(__file__), "static")
    flask_app = Flask(__name__, static_folder=static_folder_path, static_url_path="")

    if testing:
        flask_app.config.update(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            }
        )
    else:
        flask_app.config.from_object(CONFIG.get(env, ProductionConfig))

    # Initialize RESTX API
    api = Api(
        flask_app,
        version="1.0",
        title="RetroBoard V2",
        description="RetroBoard V2",
        doc="/api/docs",
        prefix="/api",
    )

    # Register API namespaces
    api.add_namespace(boards_ns)
    api.add_namespace(categories_ns)
    api.add_namespace(notes_ns)

    # Serve single-page app or static assets
    register_static_routes(flask_app)

    return flask_app


# Instantiate app for 'flask run' to detect
app = create_app()

if __name__ == "__main__":
    app.run(debug=app.debug)
