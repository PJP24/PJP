import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from notification_service.src.db.model import Base

# Set up logging from the Alembic configuration
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for autogenerate
target_metadata = Base.metadata

# Database URL from alembic.ini
url = config.get_main_option("sqlalchemy.url")

# Create an asynchronous engine
engine = create_async_engine(url, echo=True, future=True)

# Run migrations in 'offline' mode
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Run migrations in 'online' mode
async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Create an async connection to the database
    async with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        async with connection.begin():
            await context.run_migrations()

# Check if the migration is being run offline or online
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
