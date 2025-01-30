import logging
from aiosmtplib import send
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_ADDRESS = "maximvassilev01@gmail.com"
EMAIL_PASSWORD = "nymt sqha uvir lkyx"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def send_email(email: str, message: str, username: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg["Subject"] = f"Notification - PJP app for {username}"
        msg.attach(MIMEText(message, "plain"))

        logging.info(f"Email Body for {email}: {message}")

        await send(
            msg,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=EMAIL_ADDRESS,
            password=EMAIL_PASSWORD,
            use_tls=True,
        )
        logging.info(f"Email sent successfully to {email}")
    except Exception as e:
        logging.error(f"Failed to send email to {email}: {e}")
