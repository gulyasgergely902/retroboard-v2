"""Test routes"""

import unittest
from unittest.mock import ANY, MagicMock, patch

from sqlalchemy.exc import DatabaseError

from services.services import (
    add_board,
    add_category,
    add_note,
    get_board_name_from_id,
    get_boards,
    get_categories,
    get_notes,
    get_notes_for_export,
    modify_note_category,
    modify_note_tags,
    remove_board,
    remove_category,
    remove_note,
)


class TestServices(unittest.TestCase):
    """Tests for Services"""

    @patch("services.services.get_note_count_on_board")
    @patch("services.services.db")
    def test_get_boards_success(self, mock_database_handler, mock_get_count):
        """Test get boards"""
        mock_session = MagicMock()

        mock_board = MagicMock()
        mock_board.id = 10
        mock_board.name = "Test Board"

        mock_query = mock_session.query.return_value
        mock_query.all.return_value = [mock_board]

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_get_count.return_value = [(10, 3)]

        resp = get_boards()

        expected_json = [{"id": 10, "name": "Test Board", "note_count": 3}]

        self.assertEqual(resp.response, expected_json)
        self.assertEqual(resp.status_code, 200)

    @patch("services.services.db")
    def test_get_board_name_from_id_success(self, mock_database_handler):
        """Test get board name from id"""
        mock_session = MagicMock()

        mock_board = MagicMock()
        mock_board.id = 10
        mock_board.name = "Test Board"

        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_board

        mock_query = mock_session.query.return_value
        mock_query.filter.return_value = mock_filter

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        result = get_board_name_from_id(ANY)

        self.assertEqual(result, mock_board.name)

    @patch("services.services.db")
    def test_get_board_name_from_id_failure_board_not_found(
        self, mock_database_handler
    ):
        """Test get board name from id where board not found"""
        mock_session = MagicMock()

        mock_filter = MagicMock()
        mock_filter.first.return_value = None

        mock_query = mock_session.query.return_value
        mock_query.filter.return_value = mock_filter

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        result = get_board_name_from_id(ANY)

        self.assertEqual(result, "")

    @patch("services.services.Board")
    @patch("services.services.db")
    def test_add_board_success(self, mock_database_handler, mock_board_class):
        """Test add board success"""
        mock_session = MagicMock()
        mock_board = MagicMock()
        mock_board.id = 10
        mock_board_class.return_value = mock_board

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        resp = add_board(ANY)

        self.assertEqual(resp.response, {"status": "Success", "board_id": 10})
        self.assertEqual(resp.status_code, 200)

        mock_session.add.assert_called_once_with(mock_board)
        mock_session.commit.assert_called_once()

    @patch("services.services.Board")
    @patch("services.services.db")
    def test_add_board_failure(self, mock_database_handler, mock_board_class):
        """Test add board failure"""
        mock_session = MagicMock()
        mock_board = MagicMock()
        mock_board_class.return_value = mock_board

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.commit.side_effect = DatabaseError(
            "statement", {}, Exception("Error")
        )

        resp = add_board(ANY)

        self.assertIn("DB Error", resp.response["status"])  # type: ignore
        self.assertEqual(resp.status_code, 500)

        mock_session.add.assert_called_once_with(mock_board)
        mock_session.commit.assert_called_once()

    @patch("services.services.Board")
    @patch("services.services.db")
    def test_remove_board_success(self, mock_database_handler, mock_board_class):
        """Test remove board success"""
        mock_session = MagicMock()
        mock_board = MagicMock()
        mock_session.get.return_value = mock_board

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        resp = remove_board(ANY)

        self.assertEqual(resp.response, {"status": "Success"})
        self.assertEqual(resp.status_code, 200)

        mock_session.get.assert_called_once_with(mock_board_class, ANY)
        mock_session.delete.assert_called_once_with(mock_board)
        mock_session.commit.assert_called_once()

    @patch("services.services.Board")
    @patch("services.services.db")
    def test_remove_board_failure_not_found(
        self, mock_database_handler, mock_board_class
    ):
        """Test remove board where board not found"""
        mock_session = MagicMock()

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.get.return_value = None

        resp = remove_board(ANY)

        self.assertEqual(resp.response, {"status": "Board not found"})
        self.assertEqual(resp.status_code, 404)

        mock_session.get.assert_called_once_with(mock_board_class, ANY)

    @patch("services.services.Board")
    @patch("services.services.db")
    def test_remove_board_failure_database_error(
        self, mock_database_handler, mock_board_class
    ):
        """Test remove board success"""
        mock_session = MagicMock()
        mock_board = MagicMock()
        mock_session.get.return_value = mock_board

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.get.side_effect = DatabaseError(
            "statement", {}, Exception("Error")
        )

        resp = remove_board(ANY)

        self.assertIn("DB Error", resp.response["status"])  # type: ignore
        self.assertEqual(resp.status_code, 500)

        mock_session.get.assert_called_once_with(mock_board_class, ANY)
        mock_session.rollback.assert_called_once()

    @patch("services.services.db")
    def test_get_notes_success(self, mock_database_handler):
        """Test get notes"""
        mock_session = MagicMock()

        mock_note = MagicMock()
        mock_note.id = 10
        mock_note.description = "Test Note"
        mock_note.category = 10
        mock_note.tags = []

        mock_query = mock_session.query.return_value

        mock_query.where.return_value = [mock_note]

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        resp = get_notes(ANY)
        expected_json = [
            {"id": 10, "description": "Test Note", "category": 10, "tags": []}
        ]

        self.assertEqual(resp.response, expected_json)
        self.assertEqual(resp.status_code, 200)

    @patch("services.services.get_board_name_from_id")
    @patch("services.services.db")
    def test_get_notes_for_export(
        self, mock_database_handler, mock_get_board_name_from_id
    ):
        """Test get notes for export"""
        mock_session = MagicMock()

        mock_note = MagicMock()
        mock_note.description = "Test Note"
        mock_note.category = 10
        mock_get_board_name_from_id.return_value = "Sample Board"

        mock_query = mock_session.query.return_value
        mock_query.where.return_value = [mock_note]

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        result = get_notes_for_export(ANY)
        expected_json = {
            "board_name": "Sample Board",
            "notes": [{"description": "Test Note", "category": 10}],
        }

        self.assertEqual(result, expected_json)

    @patch("services.services.get_board_name_from_id")
    def test_get_notes_for_export_empty_board_name(self, mock_get_board_name_from_id):
        """Test get notes for export where board cannot be found"""
        mock_get_board_name_from_id.return_value = ""
        result = get_notes_for_export(ANY)
        self.assertEqual(result, {})

    @patch("services.services.Note")
    @patch("services.services.db")
    def test_add_note_success(self, mock_database_handler, mock_note_class):
        """Test add note success"""
        mock_session = MagicMock()
        mock_note = MagicMock()
        mock_note.id = 10
        mock_note.description = "Test Note"
        mock_note.category = 20
        mock_note.board_id = 30
        mock_note_class.return_value = mock_note

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        resp = add_note(ANY, ANY, ANY, ANY)

        self.assertEqual(resp.response, {"status": "Success"})
        self.assertEqual(resp.status_code, 200)

        mock_session.add.assert_called_once_with(mock_note)
        mock_session.commit.assert_called_once()

    @patch("services.services.Note")
    @patch("services.services.db")
    def test_add_note_failure(self, mock_database_handler, mock_note_class):
        """Test add note failure"""
        mock_session = MagicMock()
        mock_note = MagicMock()
        mock_note.id = 10
        mock_note.description = "Test Note"
        mock_note.category = 20
        mock_note.board_id = 30
        mock_note_class.return_value = mock_note

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.commit.side_effect = DatabaseError(
            "statement", {}, Exception("Error")
        )

        resp = add_note(ANY, ANY, ANY, ANY)

        self.assertIn("DB Error", resp.response["status"])  # type: ignore
        self.assertEqual(resp.status_code, 500)

        mock_session.add.assert_called_once_with(mock_note)
        mock_session.commit.assert_called_once()

    @patch("services.services.Note")
    @patch("services.services.db")
    def test_remove_note_success(self, mock_database_handler, mock_note_class):
        """Test remove note success"""
        mock_session = MagicMock()
        mock_note = MagicMock()
        mock_session.get.return_value = mock_note

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        resp = remove_note(ANY)

        self.assertEqual(resp.response, {"status": "Success"})
        self.assertEqual(resp.status_code, 200)

        mock_session.get.assert_called_once_with(mock_note_class, ANY)
        mock_session.delete.assert_called_once_with(mock_note)
        mock_session.commit.assert_called_once()

    @patch("services.services.Note")
    @patch("services.services.db")
    def test_remove_note_failure_not_found(
        self, mock_database_handler, mock_note_class
    ):
        """Ttest remove note where note not found"""
        mock_session = MagicMock()

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.get.return_value = None

        resp = remove_note(ANY)

        self.assertEqual(resp.response, {"status": "Note not found"})
        self.assertEqual(resp.status_code, 404)

        mock_session.get.assert_called_once_with(mock_note_class, ANY)

    @patch("services.services.Note")
    @patch("services.services.db")
    def test_remove_note_failure_database_error(
        self, mock_database_handler, mock_note_class
    ):
        """Test remove note success"""
        mock_session = MagicMock()
        mock_note = MagicMock()
        mock_session.get.return_value = mock_note

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.get.side_effect = DatabaseError(
            "statement", {}, Exception("Error")
        )

        resp = remove_note(ANY)

        self.assertIn("DB Error", resp.response["status"])  # type: ignore
        self.assertEqual(resp.status_code, 500)

        mock_session.get.assert_called_once_with(mock_note_class, ANY)
        mock_session.rollback.assert_called_once()

    @patch("services.services.db")
    def test_modify_note_category_success(self, mock_database_handler):
        """Test modify note category"""
        mock_session = MagicMock()
        mock_note = MagicMock()
        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_scalars = MagicMock()
        mock_scalars.one.return_value = mock_note
        mock_session.scalars.return_value = mock_scalars

        resp = modify_note_category(1, 2)

        self.assertEqual(resp.response, {"status": "Success"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mock_note.category, 2)
        mock_session.commit.assert_called_once()

    @patch("services.services.db")
    def test_modify_note_category_database_error(self, mock_database_handler):
        """Test modify note category failure"""
        mock_session = MagicMock()
        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.scalars.side_effect = DatabaseError(
            "statement", {}, Exception("Error")
        )

        resp = modify_note_category(1, 2)

        self.assertIn("DB Error", resp.response["status"])  # type: ignore
        self.assertEqual(resp.status_code, 500)
        mock_session.rollback.assert_called_once()

    @patch("services.services.db")
    def test_modify_note_tags_success(self, mock_database_handler):
        """Test modify note tag"""
        mock_session = MagicMock()
        mock_note = MagicMock()
        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_scalars = MagicMock()
        mock_scalars.one.return_value = mock_note
        mock_session.scalars.return_value = mock_scalars

        resp = modify_note_tags(1, ["sample_tag"])

        self.assertEqual(resp.response, {"status": "Success"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mock_note.tags, ["sample_tag"])
        mock_session.commit.assert_called_once()

    @patch("services.services.db")
    def test_modify_note_tags_database_error(self, mock_database_handler):
        """Test modify note tags failure"""
        mock_session = MagicMock()
        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.scalars.side_effect = DatabaseError(
            "statement", {}, Exception("Error")
        )

        resp = modify_note_tags(1, ["sample_tag"])

        self.assertIn("DB Error", resp.response["status"])  # type: ignore
        self.assertEqual(resp.status_code, 500)
        mock_session.rollback.assert_called_once()

    @patch("services.services.db")
    def test_get_categories_success(self, mock_database_handler):
        """Test get categories"""
        mock_session = MagicMock()

        mock_category = MagicMock()
        mock_category.id = 10
        mock_category.name = "Test Category"
        mock_category.board_id = 20

        mock_query = mock_session.query.return_value

        mock_query.where.return_value = [mock_category]

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        resp = get_categories(20)
        expected_json = [{"id": 10, "name": "Test Category"}]

        self.assertEqual(resp.response, expected_json)
        self.assertEqual(resp.status_code, 200)

    @patch("services.services.Category")
    @patch("services.services.db")
    def test_add_category_success(self, mock_database_handler, mock_category_class):
        """Test add category success"""
        mock_session = MagicMock()
        mock_category = MagicMock()
        mock_category.id = 10
        mock_category.name = "Test Category"
        mock_category.board_id = 20
        mock_category_class.return_value = mock_category

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        resp = add_category(ANY, ANY)

        self.assertEqual(resp.response, {"status": "Success"})
        self.assertEqual(resp.status_code, 200)

        mock_session.add.assert_called_once_with(mock_category)
        mock_session.commit.assert_called_once()

    @patch("services.services.Category")
    @patch("services.services.db")
    def test_add_category_failure(self, mock_database_handler, mock_category_class):
        """Test add category success"""
        mock_session = MagicMock()
        mock_category = MagicMock()
        mock_category.id = 10
        mock_category.name = "Test Category"
        mock_category.board_id = 20
        mock_category_class.return_value = mock_category

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.commit.side_effect = DatabaseError(
            "statement", {}, Exception("Error")
        )

        resp = add_category(ANY, ANY)

        self.assertIn("DB Error", resp.response["status"])  # type: ignore
        self.assertEqual(resp.status_code, 500)

        mock_session.add.assert_called_once_with(mock_category)
        mock_session.commit.assert_called_once()

    @patch("services.services.Category")
    @patch("services.services.db")
    def test_remove_category_success(self, mock_database_handler, mock_category_class):
        """Test remove category success"""
        mock_session = MagicMock()
        mock_category = MagicMock()
        mock_session.get.return_value = mock_category

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )
        mock_session.query.return_value.filter_by.return_value.first.return_value = None

        resp = remove_category(ANY)

        self.assertEqual(resp.response, {"status": "Success"})
        self.assertEqual(resp.status_code, 200)

        mock_session.get.assert_called_once_with(mock_category_class, ANY)
        mock_session.delete.assert_called_once_with(mock_category)
        mock_session.commit.assert_called_once()

    @patch("services.services.Category")
    @patch("services.services.db")
    def test_remove_category_failure_not_found(
        self, mock_database_handler, mock_category_class
    ):
        """Test remove category where category not found"""
        mock_session = MagicMock()

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.get.return_value = None

        resp = remove_category(ANY)

        self.assertEqual(resp.response, {"status": "Category not found"})
        self.assertEqual(resp.status_code, 404)

        mock_session.get.assert_called_once_with(mock_category_class, ANY)

    @patch("services.services.Category")
    @patch("services.services.db")
    def test_remove_category_failure_notes_associated(
        self, mock_database_handler, mock_category_class
    ):
        """Test remove category where notes are assigned to it"""
        mock_session = MagicMock()
        mock_category = MagicMock()
        mock_note = MagicMock()

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )
        mock_session.get.return_value = mock_category
        mock_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_note
        )

        resp = remove_category(ANY)

        self.assertEqual(
            resp.response,
            {"status": "Cannot delete: notes still associated with this category"},
        )
        self.assertEqual(resp.status_code, 400)

        mock_session.get.assert_called_once_with(mock_category_class, ANY)

    @patch("services.services.Category")
    @patch("services.services.db")
    def test_remove_category_failure_database_error(
        self, mock_database_handler, mock_category_class
    ):
        """Test remove note success"""
        mock_session = MagicMock()
        mock_category = MagicMock()
        mock_session.get.return_value = mock_category

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.get.side_effect = DatabaseError(
            "statement", {}, Exception("Error")
        )

        resp = remove_category(ANY)

        self.assertIn("DB Error", resp.response["status"])  # type: ignore
        self.assertEqual(resp.status_code, 500)

        mock_session.get.assert_called_once_with(mock_category_class, ANY)
        mock_session.rollback.assert_called_once()
