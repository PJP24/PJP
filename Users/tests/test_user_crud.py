import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.db.models import User
from src.db.database import Database
from src.grpc.user_crud import UserCrud
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


@pytest.mark.asyncio
async def test_read_user_return_user():
    mock_session = AsyncMock()
    mock_db = AsyncMock(Database, database_url="test_db")
    mock_user = User(id=1, username="test", email="test@test.co", password="Test123")

    with patch.object(mock_db, "session_scope", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.scalar.return_value = mock_user
        mock_session.__aexit__.return_value = None
        user_crud = UserCrud(mock_db)
        result = await user_crud.read(user_id=1)

        assert result == mock_user
        mock_session.__aenter__.assert_called_once()
        mock_session.__aexit__.assert_called_once()
        mock_session.scalar.assert_called_once()


@pytest.mark.asyncio
async def test_read_user_raise_error():
    mock_session = AsyncMock()
    mock_db = AsyncMock(Database, database_url="test_db")
    user_crud = UserCrud(mock_db)

    with patch.object(mock_db, "session_scope", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        mock_session.scalar.side_effect = SQLAlchemyError("Database error")
        with pytest.raises(SQLAlchemyError):
            await user_crud.read(user_id=1)

        mock_session.scalar.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_successfully():
    mock_session = AsyncMock()
    mock_db = AsyncMock(Database, database_url="test_db")
    mock_user = User(username="test", email="test@test.co", password="Test123")
    user_crud = UserCrud(mock_db)

    with patch.object(mock_db, "session_scope", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        result = await user_crud.create(mock_user)
        assert result == "success"

        actual_user = mock_session.add.call_args[0][0]

        assert actual_user.username == mock_user.username
        assert actual_user.email == mock_user.email
        assert actual_user.password == mock_user.password


@pytest.mark.asyncio
async def test_create_user_email_or_username_already_exists():
    mock_session = AsyncMock()
    mock_db = AsyncMock(Database, database_url="test_db")
    mock_user = User(username="test", email="test@test.co", password="Test123")
    user_crud = UserCrud(mock_db)

    with patch.object(mock_db, "session_scope", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.add = MagicMock(
            side_effect=IntegrityError(MagicMock(), MagicMock(), MagicMock())
        )
        mock_session.__aexit__.return_value = None

        result = await user_crud.create(mock_user)
        print(result)

        assert result == "Account already exists with this username/email."
        mock_session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_raise_error():
    mock_session = AsyncMock()
    mock_db = AsyncMock(Database, database_url="test_db")
    mock_user = User(username="test", email="test@test.co", password="Test123")
    user_crud = UserCrud(mock_db)

    with patch.object(mock_db, "session_scope", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        mock_session.add = MagicMock(
            side_effect=SQLAlchemyError(MagicMock(), MagicMock(), MagicMock())
        )
        with pytest.raises(SQLAlchemyError):
            await user_crud.create(mock_user)

        mock_session.add.assert_called_once()


@pytest.mark.asyncio
async def test_update_password_successfully():
    mock_session = AsyncMock()
    mock_db = AsyncMock(Database, database_url="test_db")
    user_crud = UserCrud(mock_db)

    with patch.object(mock_db, "session_scope", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        await user_crud.update_password(1, "Test111")

        mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_password_raise_error():
    mock_session = AsyncMock()
    mock_db = AsyncMock(Database, database_url="test_db")
    user_crud = UserCrud(mock_db)

    with patch.object(mock_db, "session_scope", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        mock_session.execute = MagicMock(
            side_effect=SQLAlchemyError(MagicMock(), MagicMock(), MagicMock())
        )
        with pytest.raises(SQLAlchemyError):
            await user_crud.update_password(1, "Test111")

        mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_delete_user_successfully():
    mock_session = AsyncMock()
    mock_db = AsyncMock(Database, database_url="test_db")
    user_crud = UserCrud(mock_db)

    with patch.object(mock_db, "session_scope", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        await user_crud.delete(1)

        mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_delete_user_raise_error():
    mock_session = AsyncMock()
    mock_db = AsyncMock(Database, database_url="test_db")
    user_crud = UserCrud(mock_db)

    with patch.object(mock_db, "session_scope", return_value=mock_session):
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        mock_session.execute = MagicMock(
            side_effect=SQLAlchemyError(MagicMock(), MagicMock(), MagicMock())
        )
        with pytest.raises(SQLAlchemyError):
            await user_crud.delete(1)

        mock_session.execute.assert_called_once()
