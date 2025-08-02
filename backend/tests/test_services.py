"""Test routes"""

import unittest
from unittest.mock import ANY, MagicMock, patch

from sqlalchemy.exc import DatabaseError

from services.services import (
    add_board,
    add_category,
    add_note,
    get_boards,
    get_categories,
    get_notes,
    modify_note_category,
    modify_note_tags,
    remove_board,
    remove_category,
    remove_note,
)


class TestServices(unittest.TestCase):
    """Tests for Services"""

    @patch("services.services.db")
    def test_get_boards(self, mock_database_handler):
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

        result, status_code = get_boards()
        expected_json = [{"id": 10, "name": "Test Board"}]

        self.assertEqual(result, expected_json)
        self.assertEqual(status_code, 200)

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

        result, error, status_code = add_board(ANY)

        self.assertEqual(result, {"status": "Success", "board_id": 10})
        self.assertIsNone(error)
        self.assertEqual(status_code, 200)

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

        result, error, status_code = add_board(ANY)

        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("DB Error", error["status"])  # type: ignore
        self.assertEqual(status_code, 500)

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

        result, error, status_code = remove_board(ANY)

        self.assertEqual(result, {"status": "Success"})
        self.assertIsNone(error)
        self.assertEqual(status_code, 200)

        mock_session.get.assert_called_once_with(mock_board_class, ANY)
        mock_session.delete.assert_called_once_with(mock_board)
        mock_session.commit.assert_called_once()

    @patch("services.services.Board")
    @patch("services.services.db")
    def test_remove_board_failure_not_found(
        self, mock_database_handler, mock_board_class
    ):
        """Ttest remove board where board not found"""
        mock_session = MagicMock()

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.get.return_value = None

        result, error, status_code = remove_board(ANY)

        self.assertIsNone(result)
        self.assertEqual(error, {"status": "Board not found"})
        self.assertEqual(status_code, 404)

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

        result, error, status_code = remove_board(ANY)

        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("DB Error", error["status"])  # type: ignore
        self.assertEqual(status_code, 500)

        mock_session.get.assert_called_once_with(mock_board_class, ANY)
        mock_session.rollback.assert_called_once()

    @patch("services.services.db")
    def test_get_notes(self, mock_database_handler):
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

        result, status_code = get_notes(10)
        expected_json = [
            {"id": 10, "description": "Test Note", "category": 10, "tags": []}
        ]

        self.assertEqual(result, expected_json)
        self.assertEqual(status_code, 200)

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

        result, error, status_code = add_note(ANY, ANY, ANY, ANY)

        self.assertEqual(result, {"status": "Success"})
        self.assertIsNone(error)
        self.assertEqual(status_code, 200)

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

        result, error, status_code = add_note(ANY, ANY, ANY, ANY)

        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("DB Error", error["status"])  # type: ignore
        self.assertEqual(status_code, 500)

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

        result, error, status_code = remove_note(ANY)

        self.assertEqual(result, {"status": "Success"})
        self.assertIsNone(error)
        self.assertEqual(status_code, 200)

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

        result, error, status_code = remove_note(ANY)

        self.assertIsNone(result)
        self.assertEqual(error, {"status": "Note not found"})
        self.assertEqual(status_code, 404)

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

        result, error, status_code = remove_note(ANY)

        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("DB Error", error["status"])  # type: ignore
        self.assertEqual(status_code, 500)

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

        result, error, status_code = modify_note_category(1, 2)

        self.assertEqual(result, {"status": "Success"})
        self.assertIsNone(error)
        self.assertEqual(status_code, 200)
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

        result, error, status_code = modify_note_category(1, 2)

        self.assertIsNone(result)
        self.assertIn("DB Error", error["status"])  # type: ignore
        self.assertEqual(status_code, 500)
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

        result, error, status_code = modify_note_tags(1, ["sample_tag"])

        self.assertEqual(result, {"status": "Success"})
        self.assertIsNone(error)
        self.assertEqual(status_code, 200)
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

        result, error, status_code = modify_note_tags(1, ["sample_tag"])

        self.assertIsNone(result)
        self.assertIn("DB Error", error["status"])  # type: ignore
        self.assertEqual(status_code, 500)
        mock_session.rollback.assert_called_once()

    @patch("services.services.db")
    def test_get_categories(self, mock_database_handler):
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

        result, status_code = get_categories(20)
        expected_json = [{"id": 10, "name": "Test Category"}]

        self.assertEqual(result, expected_json)
        self.assertEqual(status_code, 200)

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

        result, error, status_code = add_category(ANY, ANY)

        self.assertEqual(result, {"status": "Success"})
        self.assertIsNone(error)
        self.assertEqual(status_code, 200)

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

        result, error, status_code = add_category(ANY, ANY)

        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("DB Error", error["status"])  # type: ignore
        self.assertEqual(status_code, 500)

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

        result, error, status_code = remove_category(ANY)

        self.assertEqual(result, {"status": "Success"})
        self.assertIsNone(error)
        self.assertEqual(status_code, 200)

        mock_session.get.assert_called_once_with(mock_category_class, ANY)
        mock_session.delete.assert_called_once_with(mock_category)
        mock_session.commit.assert_called_once()

    @patch("services.services.Category")
    @patch("services.services.db")
    def test_remove_category_failure_not_found(
        self, mock_database_handler, mock_category_class
    ):
        """Ttest remove category where category not found"""
        mock_session = MagicMock()

        mock_database_handler.get_session.return_value.__enter__.return_value = (
            mock_session
        )

        mock_session.get.return_value = None

        result, error, status_code = remove_category(ANY)

        self.assertIsNone(result)
        self.assertEqual(error, {"status": "Category not found"})
        self.assertEqual(status_code, 404)

        mock_session.get.assert_called_once_with(mock_category_class, ANY)

    @patch("services.services.Category")
    @patch("services.services.db")
    def test_remove_category_failure_notes_associated(
        self, mock_database_handler, mock_category_class
    ):
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

        result, error, status_code = remove_category(ANY)

        self.assertIsNone(result)
        self.assertEqual(
            error,
            {"status": "Cannot delete: notes still associated with this category"},
        )
        self.assertEqual(status_code, 400)

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

        result, error, status_code = remove_category(ANY)

        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("DB Error", error["status"])  # type: ignore
        self.assertEqual(status_code, 500)

        mock_session.get.assert_called_once_with(mock_category_class, ANY)
        mock_session.rollback.assert_called_once()
