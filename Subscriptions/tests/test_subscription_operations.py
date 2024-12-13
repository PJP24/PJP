import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.model import Subscription
from sqlalchemy.exc import SQLAlchemyError

from src.grpc.subscription_operations import (
    create_subscription,
    get_subscriptions,
    change_subscription,
    delete_subscription,
    activate_subscription,
    deactivate_subscription,
)

# Create
@pytest.mark.asyncio
async def test_create_subscription_with_existing_email_expect_subscription_exists_error():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = Subscription(email="doesnt@matter.com", subscription_type="who_cares")
    mock_session.execute.return_value = mock_execute
    
    response = await create_subscription(mock_session, "any@email.com", "monthly")
        
    assert response.message == "\nSubscription with this email already exists."

@pytest.mark.asyncio
@patch("src.grpc.subscription_operations.validate_email", return_value=False)
async def test_create_subscription_with_invalid_email_expect_invalid_email_error(mock_validate_email):
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_execute
    
    response = await create_subscription(mock_session, "@invalid@email.com", "monthly")
        
    assert response.message == "\nInvalid email format."
    mock_validate_email.assert_called_once_with("@invalid@email.com")

@pytest.mark.asyncio
async def test_create_subscription_with_valid_email_expect_success():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_execute

    response = await create_subscription(mock_session, "valid@email.com", "monthly")

    assert response.message == "\nSubscription created."
    mock_session.add.assert_called_once()

@pytest.mark.asyncio
async def test_create_subscription_with_database_error_expect_failure():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_execute

    mock_session.add.side_effect = SQLAlchemyError("Database error")

    response = await create_subscription(mock_session, "valid@email.com", "monthly")

    assert response.message == "\nFailed to create subscription: Database error."


# Read
@pytest.mark.asyncio
async def test_get_subscriptions_expect_success():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.all.return_value = [
        Subscription(email="test1@example.com", subscription_type="monthly", is_active=True),
        Subscription(email="test2@example.com", subscription_type="yearly", is_active=False),
    ]
    mock_session.execute.return_value = mock_execute
    
    response = await get_subscriptions(mock_session)
    
    assert len(response.subscriptions) == 2


# Update
@pytest.mark.asyncio
async def test_change_subscription_with_no_subscription_found_expect_no_subscription_message():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_execute

    response = await change_subscription(mock_session, "nonexistent@email.com", "monthly")
    
    assert response.message == "\nNo subscription with this email."

@pytest.mark.asyncio
async def test_change_subscription_with_existing_subscription_expect_subscription_changed_success_message():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = Subscription(email="some@email.com", subscription_type="monthly")
    mock_session.execute = AsyncMock(return_value=mock_execute)
    
    response = await change_subscription(mock_session, "some@email.com", "yearly")
    
    assert response.message == "\nSubscription for some@email.com updated to yearly."
    assert mock_session.execute.call_count == 2

@pytest.mark.asyncio
async def test_change_subscription_with_database_error_expect_failure():
    mock_session = MagicMock(spec=AsyncSession)
    mock_execute = MagicMock()
    mock_session.execute.return_value = mock_execute
    mock_session.execute.side_effect = SQLAlchemyError("Database error")

    response = await change_subscription(mock_session, "valid@email.com", "yearly")

    assert response.message == "\nFailed to change subscription: Database error."


# Delete
@pytest.mark.asyncio
async def test_delete_subscription_with_no_subscription_found_expect_no_subscription_message():
    
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_execute

    response = await delete_subscription(mock_session, "nonexistent@email.com")
    
    assert response.message == "\nNo subscription with this email."

@pytest.mark.asyncio
async def test_delete_subscription_with_existing_subscription_expect_subscription_deleted_success_message():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = Subscription(email="some@email.com", subscription_type="monthly")
    mock_session.execute.return_value = mock_execute

    response = await delete_subscription(mock_session, "some@email.com")
    
    assert response.message == "\nSubscription deleted."

    mock_session.delete.assert_called_once()

@pytest.mark.asyncio
async def test_delete_subscription_with_database_error_expect_failure():
    mock_session = MagicMock(spec=AsyncSession)
    mock_execute = MagicMock()
    mock_session.execute.return_value = mock_execute
    mock_session.execute.side_effect = SQLAlchemyError("Database error")

    response = await delete_subscription(mock_session, "valid@email.com")

    assert response.message == "\nFailed to delete subscription: Database error."


# Activate
@pytest.mark.asyncio
async def test_activate_subscription_with_no_subscription_found_expect_no_subscription_message():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_execute
    
    response = await activate_subscription(mock_session, "any@email.com")
        
    assert response.message == "\nNo subscription with this email."    

@pytest.mark.asyncio
async def test_activate_subscription_with_active_subscription_found_expect_subscription_already_active_message():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = Subscription(email="doesnt@matter.com", subscription_type="who_cares", is_active=True)
    mock_session.execute.return_value = mock_execute
    
    response = await activate_subscription(mock_session, "doesnt@matter.com")
        
    assert response.message == "\nThe subscription for this email is already active."    

@pytest.mark.asyncio
async def test_activate_subscription_with_non_active_existing_subscription_found_expect_success_message_subscription_activated():

    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = Subscription(email="doesnt@matter.com", subscription_type="who_cares", is_active=False)
    mock_session.execute.return_value = mock_execute
    
    response = await activate_subscription(mock_session, "doesnt@matter.com")
        
    assert response.message == "\nSubscription for email doesnt@matter.com was activated."    
    
    assert mock_session.execute.call_count == 2

@pytest.mark.asyncio
async def test_activate_subscription_with_database_error_expect_failure():
    mock_session = MagicMock(spec=AsyncSession)
    mock_execute = MagicMock()
    mock_session.execute.return_value = mock_execute
    mock_session.execute.side_effect = SQLAlchemyError("Database error")

    response = await activate_subscription(mock_session, "valid@email.com")

    assert response.message == "\nFailed to activate subscription: Database error."


# Deactivate
@pytest.mark.asyncio
async def test_deactivate_subscription_with_no_subscription_found_expect_no_subscription_message():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_execute
    
    response = await deactivate_subscription(mock_session, "any@email.com")
        
    assert response.message == "\nNo subscription with this email."   


@pytest.mark.asyncio
async def test_deactivate_subscription_with_not_active_subscription_expect_no_subscription_message():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = Subscription(email="doesnt@matter.com", subscription_type="who_cares", is_active=False)
    mock_session.execute.return_value = mock_execute
    
    response = await deactivate_subscription(mock_session, "any@email.com")

    assert response.message == "\nThe subscription for this email is not active."   

@pytest.mark.asyncio
async def test_deactivate_subscription_with_active_subscription_expect_success_message_and_subscription_deactivated():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = Subscription(email="doesnt@matter.com", subscription_type="who_cares", is_active=True)
    mock_session.execute.return_value = mock_execute
    
    response = await deactivate_subscription(mock_session, "any@email.com")

    assert response.message == "\nSubscription for email any@email.com was deactivated."

    assert mock_session.execute.call_count == 2

@pytest.mark.asyncio
async def test_deactivate_subscription_with_database_error_expect_failure():
    mock_session = MagicMock(spec=AsyncSession)
    mock_execute = MagicMock()
    mock_session.execute.return_value = mock_execute
    mock_session.execute.side_effect = SQLAlchemyError("Database error")

    response = await deactivate_subscription(mock_session, "valid@email.com")

    assert response.message == "\nFailed to deactivate subscription: Database error."
