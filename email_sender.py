import smtplib
from email.message import EmailMessage
import os

def send_expense_report(
    sender_email,
    sender_password,
    recipient_email,
    subject,
    body,
    attachment_path,
    smtp_server='smtp.gmail.com',
    smtp_port=587
):
    # Build email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(body)

    # Attach CSV
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(
                file_data,
                maintype='application',
                subtype='octet-stream',
                filename=file_name
            )

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
