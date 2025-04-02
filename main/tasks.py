from celery import shared_task

@shared_task
def send_email_task(email):
    # Код отправки email
    pass