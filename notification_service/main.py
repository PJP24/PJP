import asyncio
import logging
from notification_service.consumer import consume_email_notifications
from notification_service.src.db.database import Database
from notification_service.src.config.config import TASKS_DB_URL

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_URL = TASKS_DB_URL
db = Database(DB_URL)

async def init_db(db: Database):
    try:
        await db.init_db()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing the database: {e}")
        raise

async def main():
    try:
        logging.info("Starting the email notification consumer...")
        await init_db(db)  # Ensure the DB is initialized before starting the consumer
        await consume_email_notifications()  # Start consuming Kafka messages
    except Exception as e:
        logging.error(f"Error occurred in the main execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())
