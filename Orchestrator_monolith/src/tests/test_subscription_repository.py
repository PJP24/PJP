import warnings
import pytest
from unittest.mock import MagicMock
from src.database.subscription_repositories import SubscriptionRepository

@pytest.fixture
def mock_dynamodb_client():
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_client.get_client.return_value = mock_client
    mock_client.Table.return_value = mock_table
    return mock_client, mock_table

@pytest.fixture
def repo(mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    return SubscriptionRepository(client=mock_client)

def test_get_subscription_by_user_id_success(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.get_item.return_value = {'Item': {'user_id': '123', 'subscription_type': 'premium', 'period': 'monthly'}}
    result = repo.get_subscription_by_user_id('123')
    assert result == {'user_id': '123', 'subscription_type': 'premium', 'period': 'monthly'}

def test_get_subscription_by_user_id_not_found(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.get_item.return_value = {}
    result = repo.get_subscription_by_user_id('123')
    assert result == {"error": "User not found"}

def test_get_subscription_by_user_id_exception(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.get_item.side_effect = Exception("DynamoDB error")
    result = repo.get_subscription_by_user_id('123')
    assert result == {"error": "An error occurred: DynamoDB error"}

def test_add_subscription_success(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
    result = repo.add_subscription('123', 'premium', 'monthly')
    assert result == {"user_id": '123', "subscription_type": 'premium', "period": 'monthly'}

def test_add_subscription_failure(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 400}}
    result = repo.add_subscription('123', 'premium', 'monthly')
    assert result == {"error": "Error adding user to database"}

def test_add_subscription_exception(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.put_item.side_effect = Exception("DynamoDB error")
    result = repo.add_subscription('123', 'premium', 'monthly')
    assert result == {"error": "An error occurred: DynamoDB error"}

warnings.filterwarnings("ignore", category=DeprecationWarning)