import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker
from activities import DSLActivities
from delete_user_workflow import DeleteUserWorkflow

interrupt_event = asyncio.Event()


async def main():
    client = await Client.connect("host.docker.internal:7233")
    activities = DSLActivities()
    worker = Worker(client=client, task_queue="user-service-task-queue", activities=[activities.delete_user_activity], workflows=[DeleteUserWorkflow])
    logging.info("Worker started, ctrl+c to exit")

    await worker.run()
    await interrupt_event.wait()



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())  