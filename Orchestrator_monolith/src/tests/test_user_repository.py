import warnings

import pytest
from unittest.mock import MagicMock
from src.database.connection import DynamoDBClient
from src.database.user_repositories import UserRepository

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
    return UserRepository(client=mock_client)

def test_get_user_by_user_id_success(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.get_item.return_value = {'Item': {'user_id': '123', 'name': 'John Doe', 'email': 'john@example.com'}}
    result = repo.get_user_by_user_id('123')
    assert result == {'user_id': '123', 'name': 'John Doe', 'email': 'john@example.com'}

def test_get_user_by_user_id_not_found(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.get_item.return_value = {}
    result = repo.get_user_by_user_id('123')
    assert result == {"error": "User not found"}

def test_get_user_by_user_id_exception(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.get_item.side_effect = Exception("DynamoDB error")
    result = repo.get_user_by_user_id('123')
    assert result == {"error": "An error occurred: DynamoDB error"}

def test_add_user_success(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
    result = repo.add_user('123', 'John Doe', 'john@example.com')
    assert result == {"user_id": '123', "name": 'John Doe', "email": 'john@example.com'}

def test_add_user_failure(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 400}}
    result = repo.add_user('123', 'John Doe', 'john@example.com')
    assert result == {"error": "Error adding user to database"}

def test_add_user_exception(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.put_item.side_effect = Exception("DynamoDB error")
    result = repo.add_user('123', 'John Doe', 'john@example.com')
    assert result == {"error": "An error occurred: DynamoDB error"}

def test_update_user_success(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.get_item.return_value = {'Item': {'user_id': '123', 'name': 'John Doe', 'email': 'john@example.com'}}
    mock_table.update_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}, 'Attributes': {'name': 'Jane Doe', 'email': 'jane@example.com'}}
    result = repo.update_user('123', 'Jane Doe', 'jane@example.com')
    assert result == {"user_id": '123', "name": 'Jane Doe', "email": 'jane@example.com'}

def test_update_user_not_found(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.get_item.return_value = {}
    result = repo.update_user('123', 'Jane Doe', 'jane@example.com')
    assert result == {"error": "User with user_id 123 not found"}

def test_delete_user_success(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.delete_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
    result = repo.delete_user('123')
    assert result == {"message": "User with user_id 123 deleted successfully"}

def test_delete_user_failure(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.delete_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 400}}
    result = repo.delete_user('123')
    assert result == {"error": "Error deleting user from database"}

def test_delete_user_exception(repo, mock_dynamodb_client):
    mock_client, mock_table = mock_dynamodb_client
    mock_table.delete_item.side_effect = Exception("DynamoDB error")
    result = repo.delete_user('123')
    assert result == {"error": "An error occurred: DynamoDB error"}

warnings.filterwarnings("ignore", category=DeprecationWarning)