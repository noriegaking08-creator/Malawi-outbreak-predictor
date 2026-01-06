import streamlit as st
import logging
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv


os.makedirs("data/logs", exist_ok=True)

logging.basicConfig(
    filename='data/logs/prediction_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

load_dotenv()
GMAIL_USER = os.getenv("SENDER_EMAIL")       
GMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD")       

def send_feedback_email(feedback: str):
    """Send feedback to your Gmail address."""
    try:
        msg = MIMEText(feedback)
        msg["Subject"] = "New Feedback from Streamlit App"
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_USER  

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        logging.error(f"Email sending failed: {e}")
        return False

def render_feedback():
    st.header("📝 Feedback")
    with st.form("feedback_form"):
        feedback = st.text_area("Your feedback on predictions:")
        submit = st.form_submit_button("Submit")
        if submit:
            if feedback.strip():
                logging.info(f"Feedback received: {feedback}")
                if send_feedback_email(feedback):
                    st.success("Feedback submitted successfully!")
                else:
                    st.error("Failed to send feedback. Please check your internet connection.")
            else:
                st.warning("⚠️ Please enter some feedback before submitting.")
