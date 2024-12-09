from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False, future=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
