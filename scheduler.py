import schedule
import time
import os
import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackathon2.settings")
django.setup()

from message_app.models import Message 

def log_current_message():
    now = timezone.now()
    message = Message.objects.filter(scheduled_at__lte=now).order_by('-scheduled_at').first()
    if message:
        print(f"[{now}] Current message: {message.content} (scheduled at {message.scheduled_at})")
    else:
        print(f"[{now}] No messages currently scheduled.")


schedule.every(1).minutes.do(log_current_message)

print("Scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(1)