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


#
# class Borrowing(models.Model):
#     borrow_date = models.DateField()
#     expected_return_date = models.DateField()
#     actual_return_date = models.DateField()
#     book = models.ForeignKey("Book", on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.book.title, self.expected_return_date, self.actual_return_date
#
#
# class Payment(models.Model):
#     class Status(models.TextChoices):
#         PENDING = "PENDING", "PENDING"
#         PAID = "PAID", "PAID"
#
#     class Type(models.TextChoices):
#         PAYMENT = "PAYMENT", "PAYMENT"
#         FINE = "FINE", "FINE"
#
#     status = models.CharField(max_length=10, choices=Status.choices)
#     type = models.CharField(max_length=10, choices=Type.choices)
#     borrowing = models.ForeignKey("Borrowing", on_delete=models.CASCADE)
#     session_url = models.URLField()
#     session_id = models.CharField(max_length=255)
#     money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
#
#
