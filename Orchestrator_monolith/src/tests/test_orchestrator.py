import pytest
import warnings
from unittest.mock import AsyncMock
from src.orchestrator.orchestrator import Orchestrator

@pytest.fixture
def mock_user_service_api():
    return AsyncMock()

@pytest.fixture
def mock_subscription_service_api():
    return AsyncMock()

@pytest.fixture
def orchestrator(mock_user_service_api, mock_subscription_service_api):
    return Orchestrator(user_service_api=mock_user_service_api, subscription_service_api=mock_subscription_service_api)

@pytest.mark.asyncio
async def test_get_user_success(orchestrator, mock_user_service_api):
    mock_user_service_api.fetch_user_data.return_value = {"user_id": "123", "name": "John Doe", "email": "john.doe@example.com"}

    user_data = await orchestrator.get_user("123")

    mock_user_service_api.fetch_user_data.assert_called_once_with("123")
    assert user_data == {"user_id": "123", "name": "John Doe", "email": "john.doe@example.com"}

@pytest.mark.asyncio
async def test_get_user_failure(orchestrator, mock_user_service_api):
    mock_user_service_api.fetch_user_data.side_effect = Exception("Error fetching user data")

    user_data = await orchestrator.get_user("123")

    mock_user_service_api.fetch_user_data.assert_called_once_with("123")
    assert user_data == {"error": "Error fetching user data: Error fetching user data"}

@pytest.mark.asyncio
async def test_add_user_success(orchestrator, mock_user_service_api):
    mock_user_service_api.add_user.return_value = {"user_id": "123", "name": "John Doe", "email": "john.doe@example.com"}

    user_data = await orchestrator.add_user("John Doe", "john.doe@example.com")

    mock_user_service_api.add_user.assert_called_once_with("John Doe", "john.doe@example.com")
    assert user_data == {"user_id": "123", "name": "John Doe", "email": "john.doe@example.com"}

@pytest.mark.asyncio
async def test_add_user_failure(orchestrator, mock_user_service_api):
    mock_user_service_api.add_user.side_effect = Exception("Error adding user")

    user_data = await orchestrator.add_user("John Doe", "john.doe@example.com")

    mock_user_service_api.add_user.assert_called_once_with("John Doe", "john.doe@example.com")
    assert user_data == {"error": "Error adding user: Error adding user"}

@pytest.mark.asyncio
async def test_add_subscription_success(orchestrator, mock_subscription_service_api):
    mock_subscription_service_api.add_subscription.return_value = {"user_id": "123", "subscription_type": "premium", "period": "monthly"}

    subscription_data = await orchestrator.add_subscription("premium", "monthly")

    mock_subscription_service_api.add_subscription.assert_called_once_with(subscription_type="premium", period="monthly")
    assert subscription_data == {"user_id": "123", "subscription_type": "premium", "period": "monthly"}


@pytest.mark.asyncio
async def test_add_subscription_failure(orchestrator, mock_subscription_service_api):
    mock_subscription_service_api.add_subscription.side_effect = Exception("Error adding subscription")

    subscription_data = await orchestrator.add_subscription("premium", "monthly")

    mock_subscription_service_api.add_subscription.assert_called_once_with(subscription_type="premium", period="monthly")
    assert subscription_data == {"error": "Error adding subscription: Error adding subscription"}

@pytest.mark.asyncio
async def test_update_user_success(orchestrator, mock_user_service_api):
    mock_user_service_api.update_user.return_value = {"user_id": "123", "name": "John Doe", "email": "john.doe@example.com"}

    user_data = await orchestrator.update_user("123", "John Doe", "john.doe@example.com")

    mock_user_service_api.update_user.assert_called_once_with("123", "John Doe", "john.doe@example.com")
    assert user_data == {"user_id": "123", "name": "John Doe", "email": "john.doe@example.com"}

@pytest.mark.asyncio
async def test_update_user_failure(orchestrator, mock_user_service_api):
    mock_user_service_api.update_user.side_effect = Exception("Error updating user")

    user_data = await orchestrator.update_user("123", "John Doe", "john.doe@example.com")

    mock_user_service_api.update_user.assert_called_once_with("123", "John Doe", "john.doe@example.com")
    assert user_data == {"error": "Error updating user: Error updating user"}

@pytest.mark.asyncio
async def test_delete_user_success(orchestrator, mock_user_service_api):
    mock_user_service_api.delete_user.return_value = {"user_id": "123", "message": "User deleted"}

    deletion_result = await orchestrator.delete_user("123")

    mock_user_service_api.delete_user.assert_called_once_with("123")
    assert deletion_result == {"user_id": "123", "message": "User deleted"}

@pytest.mark.asyncio
async def test_delete_user_failure(orchestrator, mock_user_service_api):
    mock_user_service_api.delete_user.side_effect = Exception("Error deleting user")

    deletion_result = await orchestrator.delete_user("123")

    mock_user_service_api.delete_user.assert_called_once_with("123")
    assert deletion_result == {"error": "Error deleting user: Error deleting user"}

warnings.filterwarnings("ignore", category=DeprecationWarning)
