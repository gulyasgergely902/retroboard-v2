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

"""All service operations"""

from sqlalchemy import func, select
from sqlalchemy.exc import DatabaseError

from custom_types.api_response import ApiResponse
from database.database_handler import DatabaseHandler
from database.models import Board, Category, Note, Setting

db = DatabaseHandler()
db.create_tables()
db.sync_settings(db.get_session())


def get_note_count_on_board():
    """Return the note count from each board"""
    with db.get_session() as session:
        counts = (
            session.query(Note.board_id, func.count().label("board_id_count"))
            .group_by(Note.board_id)
            .order_by(Note.board_id)
            .all()
        )

    return counts


def get_boards() -> ApiResponse:
    """Return all boards"""
    with db.get_session() as session:
        boards = session.query(Board).all()

    counts = get_note_count_on_board()

    boards_json = [{"id": board.id, "name": board.name} for board in boards]
    note_count_json = [
        {"board_id": item[0], "note_count": item[1]} for item in counts
    ]

    note_count_lookup = {
        item["board_id"]: item["note_count"] for item in note_count_json
    }

    merged_boards_json = []
    for board in boards_json:
        merged_boards_json.append(
            {**board, "note_count": note_count_lookup.get(board["id"], 0)}
        )

    return ApiResponse(response=merged_boards_json, status_code=200)


def get_board_name_from_id(board_id) -> str:
    """Return the name of the board from its id"""
    with db.get_session() as session:
        board = session.query(Board).filter(Board.id == board_id).first()

    if board is None:
        return ""

    return board.name


def add_board(
    board_name: str,
) -> ApiResponse:
    """Add a new board"""
    board_id = 0
    with db.get_session() as session:
        try:
            board = Board(name=board_name)
            session.add(board)
            session.commit()
            board_id = board.id
        except DatabaseError as e:
            session.rollback()
            return ApiResponse(
                response={"status": f"DB Error: {e}"}, status_code=500
            )
    return ApiResponse(
        response={"status": "Success", "board_id": board_id}, status_code=200
    )


def remove_board(
    board_id: int,
) -> ApiResponse:
    """Remove a board"""
    with db.get_session() as session:
        try:
            board = session.get(Board, board_id)
            if board is None:
                return ApiResponse(
                    response={"status": "Board not found"}, status_code=404
                )
            session.delete(board)
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return ApiResponse(
                response={"status": f"DB Error: {e}"}, status_code=500
            )
    return ApiResponse(response={"status": "Success"}, status_code=200)


def get_notes(board_id: int) -> ApiResponse:
    """Return all notes for a board"""
    with db.get_session() as session:
        notes = session.query(Note).where(Note.board_id.is_(board_id))

    notes_json = [
        {
            "id": note.id,
            "description": note.description,
            "category": note.category,
            "tags": note.tags,
        }
        for note in notes
    ]

    return ApiResponse(response=notes_json, status_code=200)


def get_notes_for_export(
    board_id: int,
) -> dict[str, str | list[dict[str, str]]]:
    """Return all notes for export from a board"""
    board_name = get_board_name_from_id(board_id)
    if board_name == "":
        return {}

    with db.get_session() as session:
        notes = session.query(Note).where(Note.board_id.is_(board_id))

    notes_json = {
        "board_name": board_name,
        "notes": [
            {
                "description": note.description,
                "category": get_category_name_from_id(note.category),
                "category_id": note.category
            }
            for note in notes
        ],
    }

    return notes_json


def add_note(
    note_description: str,
    note_category: int,
    note_tags: str,
    note_board_id: int,
) -> ApiResponse:
    """Add a new note"""
    with db.get_session() as session:
        try:
            session.add(
                Note(
                    description=note_description,
                    category=note_category,
                    tags=note_tags,
                    board_id=note_board_id,
                )
            )
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return ApiResponse(
                response={"status": f"DB Error: {e}"}, status_code=500
            )
    return ApiResponse(response={"status": "Success"}, status_code=200)


def remove_note(
    note_id: int,
) -> ApiResponse:
    """Remove a note"""
    with db.get_session() as session:
        try:
            note = session.get(Note, note_id)
            if note is None:
                return ApiResponse(
                    response={"status": "Note not found"}, status_code=404
                )
            session.delete(note)
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return ApiResponse({"status": f"DB Error: {e}"}, status_code=500)
    return ApiResponse(response={"status": "Success"}, status_code=200)


def modify_note_category(note_id: int, new_category: int) -> ApiResponse:
    """Modify a note category by id"""
    with db.get_session() as session:
        try:
            statement = select(Note).where(Note.id == note_id)
            note = session.scalars(statement).one()
            note.category = new_category
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return ApiResponse(
                response={"status": f"DB Error: {e}"}, status_code=500
            )
    return ApiResponse(response={"status": "Success"}, status_code=200)


def modify_note_tags(note_id: int, new_tags: list) -> ApiResponse:
    """Modify note tags by id"""
    with db.get_session() as session:
        try:
            statement = select(Note).where(Note.id == note_id)
            note = session.scalars(statement).one()
            note.tags = new_tags
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return ApiResponse(
                response={"status": f"DB Error: {e}"}, status_code=500
            )
    return ApiResponse(response={"status": "Success"}, status_code=200)


def get_categories(board_id: int) -> ApiResponse:
    """Return all categories for a board or all"""
    with db.get_session() as session:
        categories = session.query(Category).where(
            Category.board_id.is_(board_id)
        )

    categories_json = [
        {"id": category.id, "name": category.name} for category in categories
    ]

    return ApiResponse(response=categories_json, status_code=200)


def get_category_name_from_id(category_id) -> str:
    """Return the name of the category from its id"""
    with db.get_session() as session:
        category = (
            session.query(Category).filter(Category.id == category_id).first()
        )

    if category is None:
        return ""

    return category.name


def add_category(category_name: str, category_board_id: int) -> ApiResponse:
    """Add a new category"""
    category_id = 0
    with db.get_session() as session:
        try:
            category = Category(name=category_name, board_id=category_board_id)
            session.add(category)
            session.commit()
            category_id = category.id
        except DatabaseError as e:
            session.rollback()
            return ApiResponse(
                response={"status": f"DB Error: {e}"}, status_code=500
            )
    return ApiResponse(response={"status": "Success", "category_id": category_id}, status_code=200)


def remove_category(
    category_id: int,
) -> ApiResponse:
    """
    Remove a category by its ID.

    Returns (status, error, HTTP status code).
    """
    with db.get_session() as session:
        try:
            category = session.get(Category, category_id)
            if category is None:
                return ApiResponse(
                    response={"status": "Category not found"}, status_code=404
                )

            session.delete(category)
            session.commit()
            return ApiResponse(response={"status": "Success"}, status_code=200)
        except DatabaseError as e:
            session.rollback()
            return ApiResponse(
                response={"status": f"DB Error: {e}"}, status_code=500
            )


def get_settings() -> ApiResponse:
    """Return all settings stored"""
    with db.get_session() as session:
        settings = session.query(Setting).all()

    settings_json = [
        {
            "setting_name": setting.setting_name,
            "setting_value": setting.setting_value,
            "setting_type": setting.setting_type,
            "setting_display_name": setting.setting_display_name,
            "setting_description": setting.setting_description,
        }
        for setting in settings
    ]

    return ApiResponse(response=settings_json, status_code=200)


def modify_setting(setting_name: str, new_value: str) -> ApiResponse:
    """Modify a given setting"""
    with db.get_session() as session:
        try:
            statement = select(Setting).where(
                Setting.setting_name == setting_name
            )
            setting = session.scalars(statement).one()
            setting.setting_value = new_value
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return ApiResponse(
                response={"status": f"DB Error: {e}"}, status_code=500
            )
    return ApiResponse(response={"status": "Success"}, status_code=200)
