import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")

app = Celery("notification_system")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(
    [
        "notification_system",
    ]
)


# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
