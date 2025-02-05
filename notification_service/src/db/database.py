from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager
import logging

Base = declarative_base()

class Database:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=True, future=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def session_scope(self):
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def init_db(self):
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logging.info("Database initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing the database: {e}")
            raise
