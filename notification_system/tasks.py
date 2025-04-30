import datetime
from borrowing.models import Borrowing
from notification_system.library_bot import send_overdue_message
from library_service.celery import app
from celery.schedules import crontab


@app.task
def find_overdue_borrowings():
    expired_borrowings = Borrowing.objects.filter(
        actual_return_date__isnull=True,
        expected_return_date__lte=datetime.date.today(),
    )

    if expired_borrowings:
        users = {obj.user for obj in expired_borrowings}
        for user in users:
            overdue = expired_borrowings.filter(user=user)
            book_lst = [obj.book.title for obj in overdue]
            book_set = list(
                {
                    (
                        f"{book} x{book_lst.count(book)}"
                        if book_lst.count(book) > 1
                        else f"{book}"
                    )
                    for book in book_lst
                }
            )
            if len(overdue) > 1:
                books = "    ◦ " + ",\n    ◦ ".join(book_set)
            else:
                books = book_lst[0]
            send_overdue_message(user=user, books=books)
    else:
        send_overdue_message(overdue=False)


app.conf.beat_schedule = {
    "find-overdue-borrowings": {
        "task": "notification_system.tasks.find_overdue_borrowings",
        "schedule": crontab(hour=9, minute=0, day_of_week="mon-fri"),
    }
}
