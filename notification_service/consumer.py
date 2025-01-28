import asyncio
import json
from aiokafka import AIOKafkaConsumer
from email_sender import send_email

async def consume_email_notifications():
    consumer = AIOKafkaConsumer(
        "email_notifications",
        bootstrap_servers="broker:9092",  # Kafka broker in Docker
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )

    await consumer.start()
    try:
        print("Listening for email notifications...")
        async for message in consumer:
            email_data = message.value
            email = email_data.get("email")
            username = email_data.get("username")
            email_body = email_data.get("message")
            if email and email_body:
                await send_email(email, email_body, username)
            else:
                print(f"Invalid email data: {email_data}")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_email_notifications())
