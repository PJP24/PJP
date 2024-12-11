import unittest
from services.api import app

class TestOrchestrateInvalidInput(unittest.TestCase):
    def test_orchestrate_missing_user_id(self):
        with app.test_client() as client:
            response = client.post('/orchestrate', json={})
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json)
            self.assertEqual(response.json["error"], "user_id is required")

if __name__ == '__main__':
    unittest.main()
