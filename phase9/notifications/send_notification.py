from datetime import datetime
from pathlib import Path

print("=" * 70)
print("UK Housing Intelligence Platform")
print("Pipeline Notification")
print("=" * 70)

project_root = Path(__file__).resolve().parents[2]

notification_dir = (
    project_root
    / "phase9"
    / "notifications"
    / "logs"
)

notification_dir.mkdir(
    parents=True,
    exist_ok=True
)

notification_file = (
    notification_dir
    / "pipeline_notifications.log"
)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

message = (
    f"[{timestamp}] "
    "UK Housing Master Pipeline completed successfully.\n"
)

with open(notification_file, "a") as file:
    file.write(message)

print()

print("Notification recorded.")

print(notification_file)