from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


class Database:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False, future=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)


    @contextmanager
    async def session_scope(self):
        async with self.async_session() as session:
            try:
                yield session
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
