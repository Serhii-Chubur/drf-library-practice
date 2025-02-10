from django.db import models


# Create your models here.
class Book(models.Model):

    COVER_CHOICES = (
        ("HARD", "Hard"),
        ("SOFT", "Soft"),
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=5, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.title}, {self.author}"
