import asyncio
import logging
from consumer import consume_email_notifications

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    try:
        logging.info("Starting the email notification consumer...")
        asyncio.run(consume_email_notifications())
    except Exception as e:
        logging.error(f"Error occurred in the main execution: {e}")
