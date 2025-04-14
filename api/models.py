from django.db import models

class Customer(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    external_id_character = models.CharField(max_length=60)
    score = models.DecimalField(decimal_places=2, max_digits=10)
    preapproved_at = models.DateTimeField()

    class CustomerStatus(models.IntegerChoices):
        ACTIVE = 1, "Active"
        INACTIVE = 2, "Inactive"

    status = models.IntegerField(
        choices=CustomerStatus.choices,
        default=CustomerStatus.ACTIVE,
        verbose_name="Estado"
    )


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
        PENDING = 1, "Active"
        ACTIVE = 2, "Inactive"
        REJECTED = 3, "Rejected"
        PAID = 4, "Paid"

    status = models.IntegerField(
        choices=LoanStatus.choices,
        default=LoanStatus.PENDING,
        verbose_name="Estado"
    )


    def __str__(self):
        return self.contract_version_character




class Payment(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    external_id_character = models.CharField(max_length=60)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    paid_at = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

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
