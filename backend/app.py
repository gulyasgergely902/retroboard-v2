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


def create_app():
    """Create RetroBoard Flask Server."""
    # Base directory of this file, where 'static' folder resides
    root_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(root_dir, "static")

    flask_app = Flask(__name__, static_folder=static_dir, static_url_path="")

    # Load configuration based on FLASK_ENV
    env = os.environ.get("FLASK_ENV", "production").lower()
    if env == "production":
        flask_app.config.from_object(ProductionConfig)
    else:
        flask_app.config.from_object(DevelopmentConfig)

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
    # When running directly: python app.py
    debug_mode = app.config.get("DEBUG", False)
    app.run(debug=debug_mode)
