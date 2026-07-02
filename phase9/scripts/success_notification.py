import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

print("=" * 70)
print("UK Housing Intelligence Platform")
print("PIPELINE SUCCESS")
print("=" * 70)

print(f"Execution Time : {datetime.now()}")

print("\nPipeline Status : SUCCESS\n")

print("Completed stages\n")

print("✓ Health Check")
print("✓ Snowflake Validation")
print("✓ Data Quality Validation")
print("✓ RAW Snowflake Load")
print("✓ dbt Build")
print("✓ dbt Tests")
print("✓ Dashboard Refresh")

print("\nThe UK Housing Intelligence Platform has completed successfully.\n")

smtp_host = os.getenv("AIRFLOW__SMTP__SMTP_HOST", "smtp.gmail.com")
smtp_port = int(os.getenv("AIRFLOW__SMTP__SMTP_PORT", "587"))
smtp_user = os.getenv("AIRFLOW__SMTP__SMTP_USER")
smtp_password = os.getenv("AIRFLOW__SMTP__SMTP_PASSWORD")
mail_from = os.getenv("AIRFLOW__SMTP__SMTP_MAIL_FROM", smtp_user)

recipient = "bibhrajsaha@gmail.com"

subject = "✅ UK Housing Intelligence Platform - Pipeline Succeeded"

body = f"""
UK Housing Intelligence Platform

Pipeline Status : SUCCESS

Execution Time:
{datetime.now()}

Completed Stages

✓ Health Check
✓ Snowflake Validation
✓ Data Quality Validation
✓ RAW Snowflake Load
✓ dbt Models
✓ dbt Tests
✓ Dashboard Refresh

The complete pipeline executed successfully.
"""

msg = MIMEText(body)

msg["Subject"] = subject
msg["From"] = mail_from
msg["To"] = recipient

with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)

print("Success email sent.")