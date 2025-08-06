"""All service operations"""

from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.exc import DatabaseError

from database.database_handler import DatabaseHandler
from database.models import Board, Category, Note

db = DatabaseHandler()
db.create_tables()


def get_boards() -> tuple[list[dict[str, str]], int]:
    """Return all boards"""
    with db.get_session() as session:
        boards = session.query(Board).all()

    boards_json = [{"id": board.id, "name": board.name} for board in boards]

    return boards_json, 200


def get_board_name_from_id(board_id) -> str:
    """Return the name of the board from its id"""
    with db.get_session() as session:
        board = session.query(Board).filter(Board.id == board_id).first()

    if board is None:
        return ""

    return board.name


def add_board(
    board_name: str,
) -> tuple[Optional[dict[str, Union[str, int]]], Optional[dict[str, str]], int]:
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
            return None, {"status": f"DB Error: {e}"}, 500
    return {"status": "Success", "board_id": board_id}, None, 200


def remove_board(
    board_id: int,
) -> tuple[Optional[dict[str, str]], Optional[dict[str, str]], int]:
    """Remove a board"""
    with db.get_session() as session:
        try:
            board = session.get(Board, board_id)
            if board is None:
                return None, {"status": "Board not found"}, 404
            session.delete(board)
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return None, {"status": f"DB Error: {e}"}, 500
    return {"status": "Success"}, None, 200


def get_notes(board_id: int) -> tuple[list[dict[str, str]], int]:
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

    return notes_json, 200


def get_notes_for_export(board_id: int) -> dict[str, str | list[dict[str, str]]]:
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
                "category": note.category,
            }
            for note in notes
        ]
    }

    return notes_json


def add_note(
    note_description: str, note_category: int, note_tags: str, note_board_id: int
) -> tuple[Optional[dict[str, str]], Optional[dict[str, str]], int]:
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
            return None, {"status": f"DB Error: {e}"}, 500
    return {"status": "Success"}, None, 200


def remove_note(
    note_id: int,
) -> tuple[Optional[dict[str, str]], Optional[dict[str, str]], int]:
    """Remove a note"""
    with db.get_session() as session:
        try:
            note = session.get(Note, note_id)
            if note is None:
                return None, {"status": "Note not found"}, 404
            session.delete(note)
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return None, {"status": f"DB Error: {e}"}, 500
    return {"status": "Success"}, None, 200


def modify_note_category(
    note_id: int, new_category: int
) -> tuple[Optional[dict[str, str]], Optional[dict[str, str]], int]:
    """Modify a note category by id"""
    with db.get_session() as session:
        try:
            statement = select(Note).where(Note.id == note_id)
            note = session.scalars(statement).one()
            note.category = new_category
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return None, {"status": f"DB Error: {e}"}, 500
    return {"status": "Success"}, None, 200


def modify_note_tags(
    note_id: int, new_tags: list
) -> tuple[Optional[dict[str, str]], Optional[dict[str, str]], int]:
    """Modify note tags by id"""
    with db.get_session() as session:
        try:
            statement = select(Note).where(Note.id == note_id)
            note = session.scalars(statement).one()
            note.tags = new_tags
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return None, {"status": f"DB Error: {e}"}, 500
    return {"status": "Success"}, None, 200


def get_categories(board_id: int) -> tuple[list[dict[str, str]], int]:
    """Return all categories for a board or all"""
    with db.get_session() as session:
        categories = session.query(Category).where(
            Category.board_id.is_(board_id))

    categories_json = [
        {"id": category.id, "name": category.name} for category in categories
    ]

    return categories_json, 200


def add_category(
    category_name: str, category_board_id: int
) -> tuple[Optional[dict[str, str]], Optional[dict[str, str]], int]:
    """Add a new category"""
    with db.get_session() as session:
        try:
            session.add(Category(name=category_name,
                        board_id=category_board_id))
            session.commit()
        except DatabaseError as e:
            session.rollback()
            return None, {"status": f"DB Error: {e}"}, 500
    return {"status": "Success"}, None, 200


def remove_category(
    category_id: int,
) -> tuple[Optional[dict[str, str]], Optional[dict[str, str]], int]:
    """
    Remove a category by its ID.

    Returns (status, error, HTTP status code).
    """
    with db.get_session() as session:
        try:
            category = session.get(Category, category_id)
            if category is None:
                return None, {"status": "Category not found"}, 404

            if session.query(Note).filter_by(category=category_id).first():
                return (
                    None,
                    {
                        "status": (
                            "Cannot delete: notes still associated with this category"
                        )
                    },
                    400,
                )

            session.delete(category)
            session.commit()
            return {"status": "Success"}, None, 200
        except DatabaseError as e:
            session.rollback()
            return None, {"status": f"DB Error: {e}"}, 500
