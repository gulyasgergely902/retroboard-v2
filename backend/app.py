# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run RetroBoard server."""

import os

from flask import Flask
from flask_restx import Api

from config import DevelopmentConfig, ProductionConfig
from routes.api_routes import (
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

    api = Api(
        flask_app,
        version="1.0",
        title="RetroBoard V2",
        description="RetroBoard V2",
        doc="/api/docs",
        prefix="/api",
    )

    api.add_namespace(boards_ns)
    api.add_namespace(categories_ns)
    api.add_namespace(notes_ns)

    register_static_routes(flask_app)

    return flask_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.debug)
