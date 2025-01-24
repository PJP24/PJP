import json
import os
import asyncio
from aiokafka import AIOKafkaConsumer
from kafka.errors import KafkaError


async def save_message_to_file(message):
    output_dir = "received_messages"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    file_name = os.path.join(output_dir, f"message_{message.offset}.txt")

    with open(file_name, "w") as file:
        file.write(f"Topic: {message.topic}\n")
        file.write(f"Partition: {message.partition}\n")
        file.write(f"Offset: {message.offset}\n")
        file.write(f"Key: {message.key}\n")
        file.write(f"Value: {json.dumps(message.value)}\n")

    print(f"Message saved to {file_name}")


async def start_consumer():
    kafka_broker = "broker:9092"
    topic = "email_notifications"

    consumer = AIOKafkaConsumer(
        topic,
        loop=asyncio.get_event_loop(),
        bootstrap_servers=kafka_broker,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="notification_service_group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )

    print(f"Listening to topic '{topic}'...")

    try:
        await consumer.start()
        async for message in consumer:
            await save_message_to_file(message)
    except KeyboardInterrupt:
        print("Consumer stopped.")
    except Exception as e:
        print(f"Error in consumer: {e}")
    finally:
        await consumer.stop()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_consumer())


if __name__ == "__main__":
    main()
