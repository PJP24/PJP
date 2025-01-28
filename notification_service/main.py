import asyncio
from consumer import consume_email_notifications


if __name__ == "__main__":
    asyncio.run(consume_email_notifications())
