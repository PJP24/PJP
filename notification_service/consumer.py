import asyncio
import json
from aiokafka import AIOKafkaConsumer
from aiosmtplib import send
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 465
EMAIL_ADDRESS = "romaliiskii.v@yahoo.com"
EMAIL_PASSWORD = "qhotzruprflfebyg"


async def send_email(email: str, message: str, username: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg["Subject"] = f"Notification - PJP app for {username}"
        msg.attach(MIMEText(message, "plain"))

        await send(
            msg,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=EMAIL_ADDRESS,
            password=EMAIL_PASSWORD,
            use_tls=True,
        )
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


async def consume_email_notifications():
    consumer = AIOKafkaConsumer(
        "email_notifications",
        bootstrap_servers="broker:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="email_consumer_group",
        auto_offset_reset="earliest",
    )

    await consumer.start()
    try:
        print("Listening for email notifications...")
        async for message in consumer:
            email_data = message.value
            email = email_data.get("email")
            username = email_data.get("username")
            password = email_data.get("password")
            email_body = email_data.get("message")
            if email and email_body:
                await send_email(email, email_body, username)
                print(email, email_body, username)
            else:
                print(f"Invalid email data: {email_data}")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_email_notifications())
