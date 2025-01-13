import asyncio
from notification_service.db.models import Base
from notification_service.db.session import notification_engine

async def create_db():
    async with notification_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_db())
