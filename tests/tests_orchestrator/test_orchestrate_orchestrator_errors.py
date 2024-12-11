import unittest
from unittest.mock import patch, AsyncMock
from services.api import app

class TestOrchestrateOrchestratorErrors(unittest.TestCase):
    @patch('services.api.Orchestrator')
    def test_orchestrate_user_not_found(self, MockOrchestrator):
        mock_orchestrator = MockOrchestrator.return_value
        mock_orchestrator.execute = AsyncMock(return_value={
            "error": "An error occurred while fetching user data: No such User ID"
        })

        with app.test_client() as client:
            response = client.post('/orchestrate', json={'user_id': '999'})
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json)
            self.assertEqual(
                response.json["error"],
                "An error occurred while fetching user data: No such User ID"
            )

if __name__ == '__main__':
    unittest.main()
