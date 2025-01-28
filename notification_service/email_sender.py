from aiosmtplib import send
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 465
EMAIL_ADDRESS = "romaliiskii.v@yahoo.com"
EMAIL_PASSWORD = "tarohkfnfnmamzfz"


async def send_email(email: str, message: str, username: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg["Subject"] = f"Notification - PJP app for {username}"
        msg.attach(MIMEText(message, "plain"))

        print("Email Body:")
        print(message)

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
