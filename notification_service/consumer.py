import json
from aiokafka import AIOKafkaConsumer
from email_sender import send_email
from notification_service.src.db.models import Task, TaskStatusEnum
from notification_service.src.db.database import Database
from notification_service.src.config.config import TASKS_DB_URL

async def process_email_notification(db: Database, email_data: dict, topic: str, task_id: int):
    email = email_data.get("email")
    username = email_data.get("username")
    email_body = email_data.get("message")

    if email and email_body:
        try:
            await send_email(email, email_body, username)
            print(f"Email sent to {email} for {topic}")

            async with db.session_scope() as session:
                task = await session.get(Task, task_id)
                if task:
                    task.status = TaskStatusEnum.completed
                    session.add(task)
        except Exception as e:
            print(f"Error sending email to {email}: {e}")

            async with db.session_scope() as session:
                task = await session.get(Task, task_id)
                if task:
                    task.status = TaskStatusEnum.failed
                    session.add(task)
                    print(f"Error updating task status for {task_id}: {e}")
    else:
        print(f"Invalid email data received from {topic}, skipping.")

async def consume_email_notifications():
    db = Database(TASKS_DB_URL)  # Instantiate the database connection
    consumer = AIOKafkaConsumer(
        bootstrap_servers="broker:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )

    consumer.subscribe([
        "email_notifications",
        "successful_payment_notifications",
        "unsuccessful_payment_notifications",
        "expiring_subscriptions"
    ])

    await consumer.start()
    try:
        print("Listening for email notifications...")
        async for message in consumer:
            email_data = message.value
            if message.topic in [
                "email_notifications",
                "successful_payment_notifications",
                "unsuccessful_payment_notifications",
                "expiring_subscriptions"
            ]:
                async with db.session_scope() as session:
                    task = Task(
                        task_type=message.topic,
                        status=TaskStatusEnum.pending,
                    )
                    session.add(task)
                    await session.flush()

                    task_id = task.task_id

                await process_email_notification(db, email_data, message.topic, task_id)
    except Exception as e:
        print(f"Error in consuming Kafka messages: {e}")
    finally:
        await consumer.stop()
