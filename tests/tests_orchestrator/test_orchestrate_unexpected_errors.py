import unittest
from unittest.mock import patch, AsyncMock
from services.api import app

class TestOrchestrateUnexpectedErrors(unittest.TestCase):
    @patch('services.api.Orchestrator')
    def test_orchestrate_unexpected_error(self, MockOrchestrator):
        mock_orchestrator = MockOrchestrator.return_value
        mock_orchestrator.execute = AsyncMock(side_effect=Exception("Something went wrong"))

        with app.test_client() as client:
            response = client.post('/orchestrate', json={'user_id': '1'})
            self.assertEqual(response.status_code, 500)
            self.assertIn("error", response.json)
            self.assertTrue(response.json["error"].startswith("An unexpected error occurred"))

if __name__ == '__main__':
    unittest.main()
