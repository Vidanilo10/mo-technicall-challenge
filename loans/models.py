from django.db import models
from customers.models import Customer


class Loan(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    external_id_character = models.CharField(max_length=60)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    contract_version_character = models.CharField(max_length=30)
    maximum_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    outstanding = models.IntegerField()

    class LoanStatus(models.IntegerChoices):
        PENDING = 1, "Pending"
        ACTIVE = 2, "Active"
        REJECTED = 3, "Rejected"
        PAID = 4, "Paid"

    status = models.IntegerField(
        choices=LoanStatus.choices,
        default=LoanStatus.ACTIVE,
        verbose_name="Estado"
    )

    def __str__(self):
        return self.contract_version_character
