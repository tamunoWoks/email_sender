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
import time

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
    retries=3,  # Number of retry attempts
    retry_delay=5  # Delay between retries in seconds
):
    # Create message container
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach email body
    msg.attach(MIMEText(body, "plain"))

    # Attach file if provided
    if attachment_path:
        if not os.path.isfile(attachment_path):
            print(f"Error: The file {attachment_path} does not exist.")
            return

        filename = os.path.basename(attachment_path)
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", f"attachment; filename={filename}"
                )
                msg.attach(part)
        except Exception as e:
            print(f"Error: Failed to read attachment. {e}")
            return

    # Attempt to send the email with retries
    attempt = 0
    while attempt < retries:
        try:
            print(f"Attempt {attempt + 1} to send email...")
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(login, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            print("Email sent successfully!")
            return  # Exit function once email is successfully sent
        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed. Check your username and password.")
            break  # Authentication failure usually doesn't need retrying
        except smtplib.SMTPConnectError:
            print("Error: Unable to connect to the SMTP server.")
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()

        # Increment the attempt counter and wait before retrying
        attempt += 1
        if attempt < retries:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    print("Email sending failed after multiple attempts.")

# Sample usage
if __name__ == "__main__":
    subject = "Test Email"
    body = "This is a test email with an attachment."
    to_email = "recipient@example.com"
    from_email = "your_email@example.com"
    smtp_server = "smtp.example.com"
    smtp_port = 587
    login = "your_email@example.com"
    password = "your_password"
    attachment_path = "path_to_your_file.txt"

    send_email(
        subject,
        body,
        to_email,
        from_email,
        smtp_server,
        smtp_port,
        login,
        password,
        attachment_path,
    )
