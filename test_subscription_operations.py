import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.model import Subscription
from src.grpc.subscription_operations import create_subscription
from sqlalchemy.exc import SQLAlchemyError


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

@pytest.mark.asyncio
async def test_create_subscription_with_database_error_expect_failure():
    mock_session = MagicMock(spec=AsyncSession)
    
    mock_execute = MagicMock()
    mock_execute.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_execute

    mock_session.add.side_effect = SQLAlchemyError("Database error")

    response = await create_subscription(mock_session, "valid@email.com", "monthly")

    assert response.message == "\nFailed to create subscription: Database error."
