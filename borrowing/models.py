from django.db import models
from django.forms import ValidationError

from book.models import Book
from user.models import User


# Create your models here.
class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrowings"
    )

    def clean(self):
        if self.expected_return_date <= self.borrow_date:
            raise ValidationError(
                "Expected return date must be after borrow date."
            )
        if (
            self.actual_return_date
            and self.actual_return_date < self.borrow_date
        ):
            raise ValidationError(
                "Actual return date must be on or after borrow date."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Borrowing of {self.book.title} by {self.user.first_name} {self.user.last_name}"
