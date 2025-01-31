from apscheduler.schedulers.background import BackgroundScheduler
import time
import asyncio  # Import asyncio to run async functions
from src.orchestrator.orchestrator import Orchestrator

def test_job():
    print("Hello from APScheduler", flush=True)
    orchestrator = Orchestrator()
    
    asyncio.run(orchestrator.send_emails_for_expiring_subscriptions())

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(test_job, 'interval', seconds=30)
    scheduler.start()
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()