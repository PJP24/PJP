import json
from aiokafka import AIOKafkaConsumer
from email_sender import send_email


async def process_email_notification(email_data: dict, topic: str):
    email = email_data.get("email")
    username = email_data.get("username")
    email_body = email_data.get("message")

    if email and email_body:
        try:
            await send_email(email, email_body, username)
            print(f"Email sent to {email} for {topic}")
        except Exception as e:
            print(f"Error sending email to {email}: {e}")
    else:
        print(f"Invalid email data received from {topic}, skipping.")


async def consume_email_notifications():
    consumer = AIOKafkaConsumer(
        "email_notifications",
        bootstrap_servers="broker:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )

    consumer.subscribe([
        "email_notifications",
        "successful_payment_notifications",
        "unsuccessful_payment_notifications"
    ])

    await consumer.start()
    try:
        print("Listening for email notifications...")
        async for message in consumer:
            email_data = message.value
            if message.topic in [
                "email_notifications",
                "successful_payment_notifications",
                "unsuccessful_payment_notifications"
            ]:
                await process_email_notification(email_data, message.topic)
    except Exception as e:
        print(f"Error in consuming Kafka messages: {e}")
    finally:
        await consumer.stop()
