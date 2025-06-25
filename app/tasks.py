########################################
# app\tasks.py
########################################

# app/tasks.py
from celery import shared_task

@shared_task
def test_task():
    return "✅ Celery is working!"