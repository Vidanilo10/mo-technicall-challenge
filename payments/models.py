from django.db import models
from customers.models import Customer
from loans.models import Loan


class Payment(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    external_id_character = models.CharField(max_length=60, primary_key=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    paid_at = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_external_id = models.ForeignKey(Loan, on_delete=models.CASCADE)

    class PaymentStatus(models.IntegerChoices):
        COMPLETED = 1, "Completed"
        REJECTED = 2, "Rejected"

    status = models.IntegerField(
        choices=PaymentStatus.choices,
        verbose_name="Estado"
    )


class PaymentDetail(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
