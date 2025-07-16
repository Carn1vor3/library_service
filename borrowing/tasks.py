from celery import shared_task
from django.utils.timezone import now
from borrowing.models import Borrowing
import requests
import os


@shared_task
def send_overdue_notification():
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lt=now(), actual_return_date__isnull=True
    )

    if overdue_borrowings.exists():
        message = "⚠️ Book debtors:\n"
        for b in overdue_borrowings:
            message += f"- {b.book.title} user {b.user.email}\n"
    else:
        message = "✅ NO debts."

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=data)
    return response.json()
