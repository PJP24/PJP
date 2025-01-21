import pytest
from unittest.mock import AsyncMock
from src.db.models import User
from src.grpc.server import UserManagement
from src.grpc.generated.user_pb2 import Id, UpdatePassword, DeleteUser
from grpc import RpcError


@pytest.mark.asyncio
async def test_create_user_success():
    user_crud_mock = AsyncMock()
    user_crud_mock.create.return_value = "success"
    server = UserManagement(user_crud_mock)
    request = User(username="test1", email="test@test.co", password="Test123")
    response = await server.create(request, None)

    assert response.message == "Created user test1"

    user_crud_mock.create.assert_awaited_once_with(request)


@pytest.mark.asyncio
async def test_create_user_gRPC_error():
    user_crud_mock = AsyncMock()
    user_crud_mock.create.side_effect = RpcError("Mock RpcError.")
    server = UserManagement(user_crud_mock)
    request = User(username="test1", email="test@test.co", password="Test123")
    response = await server.create(request, None)

    assert response.message == "An error occured while processing your request."

    user_crud_mock.create.assert_awaited_once_with(request)


@pytest.mark.asyncio
async def test_read_existing_user():
    user_crud_mock = AsyncMock()
    user_crud_mock.read.return_value = User(
        id=1, username="test1", email="test@test.co", password="Test123"
    )
    server = UserManagement(user_crud_mock)
    response = await server.read(Id(id=1), None)

    assert response.username == "test1"
    assert response.email == "test@test.co"

    user_crud_mock.read.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_read_user_not_found():
    user_crud_mock = AsyncMock()
    user_crud_mock.read.return_value = None
    server = UserManagement(user_crud_mock)
    response = await server.read(Id(id=3), None)

    assert response.username == ""
    assert response.email == ""

    user_crud_mock.read.assert_awaited_once_with(3)


@pytest.mark.asyncio
async def test_update_password_successfully():
    user_crud_mock = AsyncMock()
    mock_user = User(id=1, username="test1", email="test@test.co", password="Test123")
    user_crud_mock.read.return_value = mock_user
    server = UserManagement(user_crud_mock)
    request = UpdatePassword(
        user_id=Id(id=1), old_password="Test123", new_password="Test111"
    )
    response = await server.update_password(request, None)

    assert response.message == "Password successfully updated for user with ID 1"

    user_crud_mock.update_password.assert_awaited_once_with(1, "Test111")


@pytest.mark.asyncio
async def test_update_password_user_not_found():
    user_crud_mock = AsyncMock()
    user_crud_mock.read.return_value = None
    server = UserManagement(user_crud_mock)
    request = UpdatePassword(
        user_id=Id(id=1), old_password="Test123", new_password="Test111"
    )
    response = await server.update_password(request, None)

    assert response.message == "User not found."


@pytest.mark.asyncio
async def test_update_password_passwords_not_matching():
    user_crud_mock = AsyncMock()
    mock_user = User(id=1, username="test1", email="test@test.co", password="Test123")
    user_crud_mock.read.return_value = mock_user
    server = UserManagement(user_crud_mock)
    request = UpdatePassword(
        user_id=Id(id=1), old_password="Test12", new_password="Test111"
    )
    response = await server.update_password(request, None)

    assert response.message == "Passwords do not match."


@pytest.mark.asyncio
async def test_delete_user_successfully():
    user_crud_mock = AsyncMock()
    mock_user = User(id=1, username="test1", email="test@test.co", password="Test123")
    user_crud_mock.read.return_value = mock_user
    server = UserManagement(user_crud_mock)
    request = DeleteUser(user_id=Id(id=1), confirm_delete=True)
    response = await server.delete(request, None)

    assert response.message == "User with Id 1 was deleted successfully."

    user_crud_mock.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_user_not_found():
    user_crud_mock = AsyncMock()
    user_crud_mock.read.return_value = None
    server = UserManagement(user_crud_mock)
    request = DeleteUser(user_id=Id(id=1), confirm_delete=True)
    response = await server.delete(request, None)

    assert response.message == "User not found."


@pytest.mark.asyncio
async def test_delete_user_conf_not_received():
    user_crud_mock = AsyncMock()
    mock_user = User(id=1, username="test1", email="test@test.co", password="Test123")
    user_crud_mock.read.return_value = mock_user
    server = UserManagement(user_crud_mock)
    request = DeleteUser(user_id=Id(id=1), confirm_delete=False)
    response = await server.delete(request, None)

    assert (
        response.message
        == "Delete confirmation was not received and could not delete user."
    )
