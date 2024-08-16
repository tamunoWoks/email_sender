"""
Python script designed to send an email with an optional file attachment
"""
#Import necessary modules
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(
    subject,
    body,
    to_email,
    from_email,
    smtp_server,
    smtp_port,
    login,
    password,
    attachment_path=None,
):
    # Create message container
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach email body
    msg.attach(MIMEText(body, "plain"))
