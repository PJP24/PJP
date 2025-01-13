from datetime import datetime, timedelta
from notification_service.db.models import Notification
from notification_service.db.session import NotificationSessionLocal

async def add_payment_notification(user_id: str, subscription_data: dict):
    end_date = datetime.strptime(subscription_data['end_date'], "%Y-%m-%d")
    current_date = datetime.now()
    payment_approaching_date = end_date - timedelta(days=366)

    if payment_approaching_date <= current_date < end_date:
        message = f"Payment for user_id = {user_id} is approaching in a year. Payment date: {subscription_data['end_date']}"

        async with NotificationSessionLocal() as session:
            async with session.begin():
                notification = Notification(user_id=user_id, message=message)
                session.add(notification)
                await session.commit()

        return message
    return None
