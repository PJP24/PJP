import unittest
from unittest.mock import patch
from services.api import app

class TestAPI(unittest.TestCase):

    @patch('orchestrator.orchestrator.Orchestrator.execute')
    def test_orchestrate_success(self, mock_execute):
        mock_execute.return_value = {
            "user_id": "1",
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "subscription_type": "Premium",
            "period": "12 months"
        }

        client = app.test_client()
        response = client.post('/orchestrate', json={'user_id': '1'})
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["user_id"], "1")
        self.assertEqual(data["name"], "Alice Johnson")
        self.assertEqual(data["email"], "alice.johnson@example.com")
        self.assertEqual(data["subscription_type"], "Premium")
        self.assertEqual(data["period"], "12 months")

    @patch('orchestrator.orchestrator.Orchestrator.execute')
    def test_orchestrate_user_not_found(self, mock_execute):
        mock_execute.return_value = {"error": "An error occurred while fetching user data: No such User ID"}

        client = app.test_client()
        response = client.post('/orchestrate', json={'user_id': '999'})
        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertIn("error", data)
        self.assertEqual(data["error"], "An error occurred while fetching user data: No such User ID")

    def test_orchestrate_missing_user_id(self):
        client = app.test_client()
        response = client.post('/orchestrate', json={})
        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertIn("error", data)
        self.assertEqual(data["error"], "user_id is required")

if __name__ == '__main__':
    unittest.main()
