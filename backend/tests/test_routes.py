"""Test routes"""

import unittest
from unittest.mock import patch

from app import create_app
from custom_types.api_response import ApiResponse


class TestRoutes(unittest.TestCase):
    """Tests for Routes"""

    def setUp(self):
        """Set up the test client and configure the app for testing"""
        app = create_app(testing=True)
        self.client = app.test_client()

    @patch("routes.api_routes.get_boards")
    def test_get_boards_success(self, mock_get_boards):
        """Test GET request to boards endpoint"""
        mock_json = [{"id": 1, "name": "test"}]
        mock_get_boards.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.get("/api/boards/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), mock_json)

    @patch("routes.api_routes.add_board")
    def test_post_boards_success(self, mock_add_board):
        """Test POST request to boards endpoint"""
        mock_json = {"status": "Success", "board_id": 1}
        mock_add_board.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.post("/api/boards/", json={"name": "test"})
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.add_board")
    def test_post_boards_failure(self, mock_add_board):
        """Test POST request to boards endpoint"""
        mock_json = {"status": "DB Error"}
        mock_add_board.return_value = ApiResponse(response=mock_json, status_code=500)

        response = self.client.post("/api/boards/", json={"name": "test"})
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 500)

    @patch("routes.api_routes.remove_board")
    def test_remove_boards_success(self, mock_remove_board):
        """Test REMOVE request to boards endpoint"""
        mock_json = {"status": "Success"}
        mock_remove_board.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.delete("/api/boards/?board_id=1")
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.remove_board")
    def test_remove_boards_failure(self, mock_remove_board):
        """Test REMOVE request to boards endpoint"""
        mock_json = {"status": "DB Error"}
        mock_remove_board.return_value = ApiResponse(response=mock_json, status_code=500)

        response = self.client.delete("/api/boards/?board_id=1")
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 500)

    @patch("routes.api_routes.get_notes_for_export")
    def test_get_boardsexport(self, mock_get_notes_for_export):
        """Test GET request to boards/export endpoint"""
        mock_json = {
            "board_name": "Test Board",
            "notes": [{"description": "Test note", "category": 11}],
        }
        mock_get_notes_for_export.return_value = mock_json

        response = self.client.get("/api/boards/export")
        self.assertEqual(response.get_json(), mock_json)

    @patch("routes.api_routes.get_notes")
    def test_get_notes_success(self, mock_get_notes):
        """Test GET request to notes endpoint"""
        mock_json = [{"id": 1, "description": "test", "category": 1, "tags": []}]
        mock_get_notes.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.get("/api/notes/?board_id=1")
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.add_note")
    def test_post_notes_success(self, mock_add_note):
        """Test POST request to notes endpoint"""
        mock_json = {"status": "Success"}
        mock_add_note.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.post(
            "/api/notes/",
            json={"description": "test", "category": 1, "tags": [], "board_id": 1},
        )
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.add_note")
    def test_post_notes_failure(self, mock_add_note):
        """Test POST request to notes endpoint"""
        mock_json = {"status": "DB Error"}
        mock_add_note.return_value = ApiResponse(response=mock_json, status_code=500)

        response = self.client.post(
            "/api/notes/",
            json={"description": "test", "category": 1, "tags": [], "board_id": 1},
        )
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 500)

    @patch("routes.api_routes.remove_note")
    def test_delete_notes_success(self, mock_remove_note):
        """Test DELETE request to notes endpoint"""
        mock_json = {"status": "Success"}
        mock_remove_note.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.delete("/api/notes/?note_id=1")
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.remove_note")
    def test_delete_notes_failure(self, mock_remove_note):
        """Test DELETE request to notes endpoint"""
        mock_json = {"status": "DB Error"}
        mock_remove_note.return_value = ApiResponse(response=mock_json, status_code=500)

        response = self.client.delete("/api/notes/?note_id=1")
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 500)

    @patch("routes.api_routes.modify_note_category")
    def test_put_notes_category_success(self, mock_modify_note_category):
        """Test PUT request to modify notes category endpoint"""
        mock_json = {"status": "Success"}
        mock_modify_note_category.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.put(
            "/api/notes/1/category", json={"category": "othercategory"}
        )
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.modify_note_category")
    def test_put_notes_category_failure(self, mock_modify_note_category):
        """Test PUT request to modify note category endpoint"""
        mock_json = {"status": "DB Error"}
        mock_modify_note_category.return_value = ApiResponse(response=mock_json, status_code=500)

        response = self.client.put(
            "/api/notes/1/category", json={"category": "othercategory"}
        )
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 500)

    @patch("routes.api_routes.modify_note_tags")
    def test_put_notes_tags_success(self, mock_modify_note_tags):
        """Test PUT request to modify note tags endpoint"""
        mock_json = {"status": "Success"}
        mock_modify_note_tags.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.put("/api/notes/1/tags", json={"tags": ["test_tag"]})
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.modify_note_tags")
    def test_put_notes_tags_failure(self, mock_modify_note_tags):
        """Test PUT request to modify note tags endpoint"""
        mock_json = {"status": "DB Error"}
        mock_modify_note_tags.return_value = ApiResponse(response=mock_json, status_code=500)

        response = self.client.put("/api/notes/1/tags", json={"tags": ["test_tag"]})
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 500)

    @patch("routes.api_routes.get_categories")
    def test_get_categories_success(self, mock_get_categories):
        """Test GET request to categories endpoint"""
        mock_json = [{"id": 1, "name": "test"}]
        mock_get_categories.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.get("/api/categories/?board_id=1")
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.add_category")
    def test_post_categories_success(self, mock_add_category):
        """Test POST request to categories endpoint"""
        mock_json = {"status": "Success"}
        mock_add_category.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.post(
            "/api/categories/", json={"name": "Test category", "board_id": 1}
        )
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.add_category")
    def test_post_categories_failure(self, mock_add_category):
        """Test POST request to categories endpoint"""
        mock_json = {"status": "DB Error"}
        mock_add_category.return_value = ApiResponse(response=mock_json, status_code=500)

        response = self.client.post(
            "/api/categories/", json={"name": "Test category", "board_id": 1}
        )
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 500)

    @patch("routes.api_routes.remove_category")
    def test_delete_categories_success(self, mock_remove_category):
        """Test DELETE request to categories endpoint"""
        mock_json = {"status": "Success"}
        mock_remove_category.return_value = ApiResponse(response=mock_json, status_code=200)

        response = self.client.delete("/api/categories/?category_id=1")
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 200)

    @patch("routes.api_routes.remove_category")
    def test_delete_categories_failure(self, mock_remove_category):
        """Test DELETE request to categories endpoint"""
        mock_json = {"status": "Success"}
        mock_remove_category.return_value = ApiResponse(response=mock_json, status_code=500)

        response = self.client.delete("/api/categories/?category_id=1")
        self.assertEqual(response.get_json(), mock_json)
        self.assertEqual(response.status_code, 500)
