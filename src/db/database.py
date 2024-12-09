from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db.model import Base

class Database:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False, future=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)


async def init_db(db_url):
    database = Database(database_url=db_url)
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return database
