import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def send_alert_email(recipient_email: str, body: str, subject: str = "ALERT MESSAGE FROM MALAWI OUTBREAK PREDICTOR APP") -> bool:
    """
    Sends an alert email using Gmail SMTP with app password authentication.

    Parameters:
        recipient_email (str): The email address of the recipient.
        body (str): The plain text message to send.
        subject (str): The subject of the email. Defaults to outbreak alert.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        print(" Missing sender credentials in environment variables.")
        return False

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print(" Email sent successfully!")
        return True
    except Exception as e:
        print(f" Failed to send email: {e}")
        return False
