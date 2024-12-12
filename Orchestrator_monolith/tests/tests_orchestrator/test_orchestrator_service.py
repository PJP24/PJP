import unittest
from unittest.mock import AsyncMock, patch
from orchestrator.orchestrator import Orchestrator


class TestOrchestrator(unittest.IsolatedAsyncioTestCase):
    @patch('orchestrator.orchestrator.get_user_service_api')
    @patch('orchestrator.orchestrator.get_subscription_service_api')
    async def test_orchestrate_success(self, mock_subscription_service, mock_user_service):
        mock_user_service.return_value.fetch_user_data = AsyncMock(
            return_value={'user_id': '1', 'name': 'John Doe', 'email': 'john@example.com'})
        mock_subscription_service.return_value.fetch_subscription_data = AsyncMock(
            return_value={'subscription_type': 'Premium', 'period': 'Yearly'})

        orchestrator = Orchestrator()
        response = await orchestrator.execute('1')

        self.assertTrue('user_id' in response and response['user_id'] == '1')
        self.assertTrue('name' in response and response['name'] == 'John Doe')
        self.assertTrue('subscription_type' in response and response['subscription_type'] == 'Premium')
        self.assertTrue('email' in response and response['email'] == 'john@example.com')
        self.assertTrue('period' in response and response['period'] == 'Yearly')

    @patch('orchestrator.orchestrator.get_user_service_api')
    @patch('orchestrator.orchestrator.get_subscription_service_api')
    async def test_orchestrate_user_error(self, mock_subscription_service, mock_user_service):
        mock_user_service.return_value.fetch_user_data = AsyncMock(return_value={'error': 'No user found'})
        mock_subscription_service.return_value.fetch_subscription_data = AsyncMock(
            return_value={'subscription_type': 'Premium', 'period': 'Yearly'})

        orchestrator = Orchestrator()
        response = await orchestrator.execute('1')

        self.assertTrue('error' in response and response['error'] == "No user found")

    @patch('orchestrator.orchestrator.get_user_service_api')
    @patch('orchestrator.orchestrator.get_subscription_service_api')
    async def test_orchestrate_subscription_error(self, mock_subscription_service, mock_user_service):
        mock_user_service.return_value.fetch_user_data = AsyncMock(
            return_value={'user_id': '1', 'name': 'John Doe', 'email': 'john@example.com'})
        mock_subscription_service.return_value.fetch_subscription_data = AsyncMock(
            return_value={'error': 'No subscription found'})

        orchestrator = Orchestrator()
        response = await orchestrator.execute('1')

        self.assertTrue('error' in response and response['error'] == "No subscription found")

    @patch('orchestrator.orchestrator.get_user_service_api')
    @patch('orchestrator.orchestrator.get_subscription_service_api')
    async def test_orchestrate_both_errors(self, mock_subscription_service, mock_user_service):
        mock_user_service.return_value.fetch_user_data = AsyncMock(return_value={'error': 'No user found'})
        mock_subscription_service.return_value.fetch_subscription_data = AsyncMock(
            return_value={'error': 'No subscription found'})

        orchestrator = Orchestrator()
        response = await orchestrator.execute('1')

        self.assertTrue('error' in response and response['error'] == "No user found | No subscription found")

    @patch('orchestrator.orchestrator.get_user_service_api')
    @patch('orchestrator.orchestrator.get_subscription_service_api')
    async def test_orchestrator_empty_data(self, mock_subscription_service, mock_user_service):
        mock_user_service.return_value.fetch_user_data = AsyncMock(return_value={'error': 'No such User ID'})
        mock_subscription_service.return_value.fetch_subscription_data = AsyncMock(
            return_value={'error': 'No such Subscription ID'})

        orchestrator = Orchestrator()
        response = await orchestrator.execute('1')

        self.assertTrue('error' in response and response['error'] == "No such User ID | No such Subscription ID")

    @patch('orchestrator.orchestrator.get_user_service_api')
    @patch('orchestrator.orchestrator.get_subscription_service_api')
    async def test_orchestrator_exception_handling(self, mock_subscription_service, mock_user_service):
        mock_user_service.return_value.fetch_user_data = AsyncMock(side_effect=Exception("User service failure"))
        mock_subscription_service.return_value.fetch_subscription_data = AsyncMock(
            side_effect=Exception("Subscription service failure"))

        orchestrator = Orchestrator()
        response = await orchestrator.execute('1')

        self.assertTrue('error' in response)
        self.assertIn("An error occurred while fetching user data", response["error"])
        self.assertIn("An error occurred while fetching subscription data", response["error"])


if __name__ == '__main__':
    unittest.main()
