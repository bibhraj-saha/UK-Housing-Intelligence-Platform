import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

print("=" * 70)
print("UK Housing Intelligence Platform")
print("PIPELINE FAILURE")
print("=" * 70)

print(f"Execution Time : {datetime.now()}")

print("\nPipeline Status : FAILED\n")

print("One or more tasks failed during pipeline execution.\n")

smtp_host = os.getenv("AIRFLOW__SMTP__SMTP_HOST", "smtp.gmail.com")
smtp_port = int(os.getenv("AIRFLOW__SMTP__SMTP_PORT", "587"))
smtp_user = os.getenv("AIRFLOW__SMTP__SMTP_USER")
smtp_password = os.getenv("AIRFLOW__SMTP__SMTP_PASSWORD")
mail_from = os.getenv("AIRFLOW__SMTP__SMTP_MAIL_FROM", smtp_user)

recipient = "bibhrajsaha@gmail.com"

subject = "❌ UK Housing Intelligence Platform - Pipeline Failed"

body = f"""
UK Housing Intelligence Platform

Pipeline Status : FAILED

Execution Time:
{datetime.now()}

One or more tasks failed.

Please review the Airflow logs for details.
"""

msg = MIMEText(body)

msg["Subject"] = subject
msg["From"] = mail_from
msg["To"] = recipient

with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)

print("Failure email sent.")