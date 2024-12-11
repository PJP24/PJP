import unittest
from unittest.mock import patch, AsyncMock
from services.api import app

class TestOrchestrateValid(unittest.TestCase):
    @patch('services.api.Orchestrator')
    def test_orchestrate_success(self, MockOrchestrator):
        mock_orchestrator = MockOrchestrator.return_value
        mock_orchestrator.execute = AsyncMock(return_value={
            "user_id": "1",
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "subscription_type": "Premium",
            "period": "12 months"
        })

        with app.test_client() as client:
            response = client.post('/orchestrate', json={'user_id': '1'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["user_id"], "1")
            self.assertEqual(response.json["name"], "Alice Johnson")

if __name__ == '__main__':
    unittest.main()
