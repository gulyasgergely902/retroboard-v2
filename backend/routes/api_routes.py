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

"""Routes for RetroBoard Server"""

import json
from datetime import datetime

from flask import Response, request, send_from_directory
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.exceptions import NotFound

from services.services import (
    add_board,
    add_category,
    add_note,
    get_board_name_from_id,
    get_boards,
    get_categories,
    get_notes,
    get_notes_for_export,
    get_settings,
    modify_note_category,
    modify_note_tags,
    modify_setting,
    remove_board,
    remove_category,
    remove_note,
)

boards_ns = Namespace("boards", description="Board related operations")

board_model = boards_ns.model("Board", {"name": fields.String(required=True)})


@boards_ns.route("/")
class Boards(Resource):
    """All boards related endpoints"""

    def get(self):
        """Get all boards"""
        resp = get_boards()
        return resp.response, resp.status_code

    @boards_ns.expect(board_model)
    def post(self):
        """Add a new board"""
        data = request.get_json()
        resp = add_board(data["name"])
        return resp.response, resp.status_code

    def delete(self):
        """Remove a board by id"""
        parser = reqparse.RequestParser()
        parser.add_argument("board_id", type=int)
        args = parser.parse_args()
        resp = remove_board(args["board_id"])
        return resp.response, resp.status_code


@boards_ns.route("/export")
class BoardsExport(Resource):
    """Export a board"""

    def get(self):
        """Get and serve for export all notes from a board"""
        parser = reqparse.RequestParser()
        parser.add_argument("board_id", type=int)
        args = parser.parse_args()
        result = get_notes_for_export(args["board_id"])
        export_data = json.dumps(result, indent=2)
        response = Response(
            export_data.encode("utf-8"),
            mimetype="application/json",
            status=200,
        )
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        board_name = get_board_name_from_id(args["board_id"])
        filename = f"export_{timestamp}_{board_name}.json"

        response.headers["Content-Disposition"] = (
            f"attachment; filename={filename}"
        )
        return response


notes_ns = Namespace("notes", description="Note related operations")

note_model = notes_ns.model(
    "Note",
    {
        "description": fields.String(required=True),
        "category": fields.Integer(required=True),
        "tags": fields.List(fields.String, required=False),
        "board_id": fields.Integer(required=True),
    },
)

category_model = notes_ns.model(
    "CategoryUpdate",
    {"category": fields.Integer(required=True, description="New category")},
)

tags_model = notes_ns.model(
    "TagsUpdate",
    {
        "tags": fields.List(
            fields.String, required=True, description="New tags"
        )
    },
)


@notes_ns.route("/")
class Notes(Resource):
    """All notes related endpoints"""

    def get(self):
        """Get notes for a given board"""
        parser = reqparse.RequestParser()
        parser.add_argument("board_id", type=int)
        args = parser.parse_args()
        resp = get_notes(args["board_id"])
        return resp.response, resp.status_code

    @notes_ns.expect(note_model)
    def post(self):
        """Add a new note"""
        data = request.get_json()
        resp = add_note(
            data["description"],
            data["category"],
            data.get("tags", []),
            data["board_id"],
        )
        return resp.response, resp.status_code

    def delete(self):
        """Remove a note by id"""
        parser = reqparse.RequestParser()
        parser.add_argument("note_id", type=int)
        args = parser.parse_args()
        resp = remove_note(args["note_id"])
        return resp.response, resp.status_code


@notes_ns.route("/<int:note_id>/category")
class NoteCategoryResource(Resource):
    """Modify a note category"""

    @notes_ns.expect(category_model)
    def put(self, note_id):
        """Update the category of a note"""
        data = request.get_json()
        new_category = data.get("category")

        resp = modify_note_category(note_id, new_category)
        return resp.response, resp.status_code


@notes_ns.route("/<int:note_id>/tags")
class NoteTagsResource(Resource):
    """Modify a note tags"""

    @notes_ns.expect(tags_model)
    def put(self, note_id):
        """Update the tags of a note"""
        data = request.get_json()
        new_tags = data.get("tags")

        resp = modify_note_tags(note_id, new_tags)
        return resp.response, resp.status_code


categories_ns = Namespace(
    "categories", description="Category related operation"
)

category_model = categories_ns.model(
    "Category",
    {
        "id": fields.Integer(required=True, description="Category ID"),
        "name": fields.String(required=True),
        "board_id": fields.Integer(required=True),
    },
)


@categories_ns.route("/")
class Categories(Resource):
    """All category related endpoints"""

    def get(self):
        """Get all categories or for a given board"""
        parser = reqparse.RequestParser()
        parser.add_argument("board_id", type=int)
        args = parser.parse_args()
        resp = get_categories(args["board_id"])
        return resp.response, resp.status_code

    @notes_ns.expect(category_model)
    def post(self):
        """Add a new category"""
        data = request.get_json()
        resp = add_category(data["name"], data["board_id"])
        return resp.response, resp.status_code

    def delete(self):
        """Delete a category by id"""
        parser = reqparse.RequestParser()
        parser.add_argument("category_id")
        args = parser.parse_args()
        resp = remove_category(args["category_id"])
        return resp.response, resp.status_code


settings_ns = Namespace("settings", description="Settings related operations")

setting_model = settings_ns.model(
    "Setting",
    {
        "setting_name": fields.String(required=True),
        "setting_value": fields.Integer(required=True),
    },
)


@settings_ns.route("/")
class Settings(Resource):
    """All settings related endpoints"""

    def get(self):
        """Get all settings"""
        resp = get_settings()
        return resp.response, resp.status_code


@settings_ns.route("/<string:setting_name>")
class ModifyStringSetting(Resource):
    """Modify a string setting"""

    def put(self, setting_name):
        """Update the tags of a note"""
        data = request.get_json()
        new_value = data.get("new_value")

        resp = modify_setting(setting_name, new_value)
        return resp.response, resp.status_code


def register_static_routes(app):
    """Register static routes for serving static files"""

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_vue(path):
        """Server static files"""
        if path.startswith("api/"):
            raise NotFound()

        try:
            return send_from_directory(app.static_folder, path)
        except NotFound:
            return send_from_directory(app.static_folder, "index.html")
