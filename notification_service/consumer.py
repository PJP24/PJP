import json
from aiokafka import AIOKafkaConsumer
from email_sender import send_email
# from notification_service.src.db.database import TasksDatabase
# from notification_service.src.db.model import Task
# from notification_service.src.config.config import TASKS_DB_URL


# TASKS_DB_URLdb = TasksDatabase(TASKS_DB_URL)


async def consume_email_notifications():
    consumer = AIOKafkaConsumer(
        "email_notifications", 
        bootstrap_servers="broker:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )

    consumer.subscribe(["email_notifications", "successful_payment_notifications"])

    await consumer.start()
    try:
        print("Listening for email notifications...")
        async for message in consumer:
            if message.topic == "email_notifications":
                email_data = message.value
                email = email_data.get("email")
                username = email_data.get("username")
                email_body = email_data.get("message")

            # if email and email_body:
            #     async with db.session_scope() as session:
            #         task = Task(
            #             email=email,
            #             username=username,
            #             message=email_body
            #         )
            #         session.add(task)
            #         await session.commit()
            #     print(f"Task saved for {email}")
            elif message.topic == "successful_payment_notifications":
                email_data = message.value
                email = email_data.get("email")
                username = email_data.get("username")
                email_body = email_data.get("message")
            await send_email(email, email_body, username)
            # else:
            #     print(f"Invalid email data: {email_data}")
    finally:
        await consumer.stop()

