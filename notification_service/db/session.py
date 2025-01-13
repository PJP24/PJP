from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///notification_service/db/notifications.db"

notification_engine = create_async_engine(DATABASE_URL, echo=True, future=True)
NotificationSessionLocal = sessionmaker(notification_engine, class_=AsyncSession, expire_on_commit=False)