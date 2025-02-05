from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import activity, workflow
import asyncio
import uuid
from datetime import timedelta

@workflow.defn
class UserSubscriptionWorkflow:
    @workflow.run
    async def run(self):
        await workflow.execute_activity(
            create_user,
            start_to_close_timeout=timedelta(seconds=10)
        )
        await workflow.execute_activity(
            add_subscription,
            start_to_close_timeout=timedelta(seconds=10)
        )

        await workflow.execute_activity(
            activate_subscription,
            start_to_close_timeout=timedelta(seconds=10)
        )

@activity.defn
async def create_user():
    print("Creating user ...")

@activity.defn
async def add_subscription():
    print("Creating subscription ...")

@activity.defn
async def activate_subscription():
    print("Activating subscription ...")

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(client, task_queue="user_subscription_queue", workflows=[UserSubscriptionWorkflow], activities=[create_user, add_subscription, activate_subscription])

    worker_task = asyncio.create_task(worker.run())
    unique_id = f"user-subscription-workflow-{uuid.uuid4()}"
    await client.execute_workflow(
        UserSubscriptionWorkflow.run,
        id=unique_id,
        task_queue="user_subscription_queue"
    )
    await worker_task

if __name__ == "__main__":
    asyncio.run(main())
