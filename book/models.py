from django.db import models


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = "HARD", "HARD"
        SOFT = "SOFT", "SOFT"

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=100, choices=Cover.choices)
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title}, {self.author}"
