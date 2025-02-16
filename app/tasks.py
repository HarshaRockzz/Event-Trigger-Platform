from celery import Celery
import os

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://event-trigger-platform-redis-1:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://event-trigger-platform-redis-1:6379/0")
)

@celery_app.task
def schedule_event(trigger_id: int):
    print(f"Trigger {trigger_id} executed")
