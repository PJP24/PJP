import unittest
from unittest.mock import MagicMock, patch
from orchestrator.factories import get_user_service_api, get_subscription_service_api


class TestFactories(unittest.TestCase):

    @patch('orchestrator.factories.UserServiceAPI')
    def test_get_user_service_api(self, MockUserServiceAPI):
        mock_instance = MagicMock()
        MockUserServiceAPI.return_value = mock_instance

        result = get_user_service_api()

        self.assertEqual(result, mock_instance)
        MockUserServiceAPI.assert_called_once_with(host="user_service:50051")

    @patch('orchestrator.factories.SubscriptionServiceAPI')
    def test_get_subscription_service_api(self, MockSubscriptionServiceAPI):
        mock_instance = MagicMock()
        MockSubscriptionServiceAPI.return_value = mock_instance

        result = get_subscription_service_api()

        self.assertEqual(result, mock_instance)
        MockSubscriptionServiceAPI.assert_called_once_with(host="subscription_service:50052")


if __name__ == '__main__':
    unittest.main()
