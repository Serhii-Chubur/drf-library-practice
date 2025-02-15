import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")

app = Celery("library_service")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(
    [
        "notification_system",
    ]
)


app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
